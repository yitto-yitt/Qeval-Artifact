# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq

def sampler_qiskit() -> Dict[str, float]:
    def _call_if_exists(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)(*args)
        raise AttributeError(names[0])

    def _alloc_many(machine, many_names, single_names, n):
        for name in many_names:
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        for name in single_names:
            if hasattr(machine, name):
                alloc = getattr(machine, name)
                return [alloc() for _ in range(n)]
        raise AttributeError(many_names[0])

    def _append(prog, op):
        try:
            prog << op
        except Exception:
            if hasattr(prog, "insert"):
                prog.insert(op)
            else:
                raise

    def _build_program(with_measurements=False):
        p = pq.QProg()
        h_gate = getattr(pq, "H")
        cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")
        _append(p, h_gate(qubits[0]))
        _append(p, cnot_gate(qubits[0], qubits[1]))
        if with_measurements:
            done = False
            for mname in ("measure_all", "MeasureAll"):
                if hasattr(pq, mname):
                    try:
                        _append(p, getattr(pq, mname)(qubits, cbits))
                        done = True
                        break
                    except Exception:
                        pass
            if not done:
                measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure")
                _append(p, measure_gate(qubits[0], cbits[0]))
                _append(p, measure_gate(qubits[1], cbits[1]))
        return p

    def _distribution(raw):
        if raw is None:
            return None
        if isinstance(raw, dict):
            items = list(raw.items())
        else:
            try:
                seq = list(raw)
            except TypeError:
                return None
            if all(isinstance(x, (int, float, complex)) or hasattr(x, "item") for x in seq):
                items = [(i, v) for i, v in enumerate(seq)]
            else:
                items = seq

        out = {}
        for k, v in items:
            if hasattr(v, "item"):
                v = v.item()
            if isinstance(v, complex):
                v = abs(v)
            v = float(v)
            if v <= 1e-12:
                continue

            if isinstance(k, int):
                key = format(k, "02b")
            else:
                key = str(k).replace(" ", "")
                if key.startswith("0b"):
                    key = key[2:]
                if all(ch in "01" for ch in key):
                    key = key.zfill(2)[-2:]
                else:
                    try:
                        key = format(int(key), "02b")
                    except Exception:
                        pass
            out[key] = out.get(key, 0.0) + v

        total = sum(out.values())
        if total == 0:
            return None
        return {k: v / total for k, v in out.items()}

    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
            except TypeError:
                pass
            break

    for obj, seed_name in ((machine, "set_random_seed"), (machine, "set_seed"), (pq, "set_random_seed"), (pq, "set_seed")):
        if hasattr(obj, seed_name):
            try:
                getattr(obj, seed_name)(42)
            except Exception:
                pass

    qubits = _alloc_many(machine, ("qAlloc_many", "qalloc_many", "qAllocMany"), ("qAlloc", "qalloc"), 2)
    cbits = _alloc_many(machine, ("cAlloc_many", "calloc_many", "cAllocMany"), ("cAlloc", "calloc"), 2)

    prog = _build_program(False)

    for args in ((prog, qubits, -1), (prog, qubits)):
        if hasattr(machine, "prob_run_dict"):
            try:
                dist = _distribution(machine.prob_run_dict(*args))
                if dist:
                    return dist
            except Exception:
                pass

    if hasattr(machine, "prob_run_list"):
        for args in ((prog, qubits, -1), (prog, qubits)):
            try:
                dist = _distribution(machine.prob_run_list(*args))
                if dist:
                    return dist
            except Exception:
                pass

    meas_prog = _build_program(True)
    shots = 4096

    if hasattr(machine, "run_with_configuration"):
        for args in ((meas_prog, cbits, shots), (meas_prog, shots, cbits), (meas_prog, shots)):
            try:
                dist = _distribution(machine.run_with_configuration(*args))
                if dist:
                    return dist
            except Exception:
                pass

    if hasattr(machine, "run"):
        for kwargs in ({"shots": shots}, {"shot": shots}, {}):
            try:
                dist = _distribution(machine.run(meas_prog, **kwargs))
                if dist:
                    return dist
            except Exception:
                pass
        for args in ((meas_prog, shots), (meas_prog, cbits, shots), (meas_prog, shots, cbits)):
            try:
                dist = _distribution(machine.run(*args))
                if dist:
                    return dist
            except Exception:
                pass

    raise RuntimeError("Unable to execute Bell circuit with pyqpanda3")
