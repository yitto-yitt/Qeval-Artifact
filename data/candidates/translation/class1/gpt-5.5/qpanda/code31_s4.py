# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq

def sampler_qiskit() -> Dict[str, float]:
    def _try_call(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                try:
                    return getattr(obj, name)(*args)
                except Exception:
                    pass
        return None

    def _append(prog, op):
        try:
            return prog << op
        except Exception:
            try:
                prog.insert(op)
                return prog
            except Exception:
                raise

    def _as_distribution(result):
        if result is None:
            return None

        data = {}
        if isinstance(result, dict):
            items = result.items()
        elif isinstance(result, (list, tuple)):
            items = enumerate(result)
        else:
            return None

        for key, value in items:
            try:
                value = float(value)
            except Exception:
                try:
                    value = float(abs(value))
                except Exception:
                    continue

            if isinstance(key, int):
                bitstr = format(key, "02b")
            elif isinstance(key, (tuple, list)):
                bitstr = "".join(str(int(x)) for x in key)
            else:
                bitstr = str(key).replace(" ", "")

            if len(bitstr) < 2:
                bitstr = bitstr.zfill(2)
            elif len(bitstr) > 2:
                bitstr = bitstr[-2:]

            if value > 1e-12:
                data[bitstr] = data.get(bitstr, 0.0) + value

        total = sum(data.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in data.items()}

    qvm = pq.CPUQVM()
    _try_call(qvm, ("init_qvm", "init", "initQVM"))

    for target in (pq, qvm):
        _try_call(target, ("set_random_seed", "set_seed", "set_random_engine_seed", "set_simulator_seed"), 42)

    qubits = _try_call(qvm, ("qAlloc_many", "qAllocMany", "qalloc_many", "allocate_qubits", "alloc_many_qubits"), 2)
    if qubits is None and hasattr(pq, "qAlloc_many"):
        qubits = pq.qAlloc_many(2)

    prog = pq.QProg()
    prog = _append(prog, pq.H(qubits[0]))
    if hasattr(pq, "CNOT"):
        prog = _append(prog, pq.CNOT(qubits[0], qubits[1]))
    else:
        prog = _append(prog, pq.CX(qubits[0], qubits[1]))

    for args in ((prog, qubits, -1), (prog, qubits)):
        result = _try_call(qvm, ("prob_run_dict", "prob_run_list", "probRunDict", "probRunList"), *args)
        dist = _as_distribution(result)
        if dist is not None:
            _try_call(qvm, ("finalize", "finalize_qvm"))
            return dist

    _try_call(qvm, ("directly_run", "directlyRun", "run"), prog)
    for args in ((qubits, -1), (qubits,)):
        result = _try_call(qvm, ("get_prob_dict", "get_prob_list", "getProbDict", "getProbList"), *args)
        dist = _as_distribution(result)
        if dist is not None:
            _try_call(qvm, ("finalize", "finalize_qvm"))
            return dist

    cbits = _try_call(qvm, ("cAlloc_many", "cAllocMany", "calloc_many", "allocate_cbits", "alloc_many_cbits"), 2)
    if cbits is None and hasattr(pq, "cAlloc_many"):
        cbits = pq.cAlloc_many(2)

    meas_prog = pq.QProg()
    meas_prog = _append(meas_prog, pq.H(qubits[0]))
    if hasattr(pq, "CNOT"):
        meas_prog = _append(meas_prog, pq.CNOT(qubits[0], qubits[1]))
    else:
        meas_prog = _append(meas_prog, pq.CX(qubits[0], qubits[1]))

    if hasattr(pq, "measure_all"):
        meas_prog = _append(meas_prog, pq.measure_all(qubits, cbits))
    else:
        measure_gate = getattr(pq, "Measure", getattr(pq, "measure", None))
        meas_prog = _append(meas_prog, measure_gate(qubits[0], cbits[0]))
        meas_prog = _append(meas_prog, measure_gate(qubits[1], cbits[1]))

    shots = 4096
    for args in ((meas_prog, cbits, shots), (meas_prog, shots)):
        result = _try_call(qvm, ("run_with_configuration", "runWithConfiguration", "run"), *args)
        dist = _as_distribution(result)
        if dist is not None:
            _try_call(qvm, ("finalize", "finalize_qvm"))
            return dist

    result = _try_call(pq, ("run_with_configuration", "runWithConfiguration"), meas_prog, cbits, shots)
    dist = _as_distribution(result)
    _try_call(qvm, ("finalize", "finalize_qvm"))
    if dist is None:
        raise RuntimeError("Unable to execute pyQPanda3 Bell sampler.")
    return dist
