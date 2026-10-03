# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq


def bell_each_shot():
    shots = 10

    def _make_machine():
        for name in ("CPUQVM", "CPUSingleThreadQVM"):
            if hasattr(pq, name):
                m = getattr(pq, name)()
                for init_name in ("init_qvm", "initQVM", "init"):
                    if hasattr(m, init_name):
                        try:
                            getattr(m, init_name)()
                        except TypeError:
                            pass
                        break
                return m
        raise RuntimeError("No suitable pyQPanda3 quantum machine found")

    def _alloc_many(machine, n, is_cbit=False):
        names = (
            ("cAlloc_many", "cAllocMany", "calloc_many", "c_alloc_many", "cAlloc")
            if is_cbit
            else ("qAlloc_many", "qAllocMany", "qalloc_many", "q_alloc_many", "qAlloc")
        )
        for name in names:
            if hasattr(machine, name):
                meth = getattr(machine, name)
                try:
                    obj = meth(n)
                    if isinstance(obj, (list, tuple)) or hasattr(obj, "__getitem__"):
                        return obj
                except TypeError:
                    pass
                try:
                    return [meth() for _ in range(n)]
                except TypeError:
                    pass
        raise RuntimeError("Allocation failed")

    def _append(prog, op):
        if hasattr(prog, "insert"):
            try:
                prog.insert(op)
                return
            except Exception:
                pass
        prog.__lshift__(op)

    def _build_program(with_measure=True):
        machine = _make_machine()
        qubits = _alloc_many(machine, 2, False)
        cbits = _alloc_many(machine, 2, True)
        prog = pq.QProg()
        _append(prog, pq.H(qubits[0]))
        if hasattr(pq, "CNOT"):
            _append(prog, pq.CNOT(qubits[0], qubits[1]))
        else:
            _append(prog, pq.CX(qubits[0], qubits[1]))
        if with_measure:
            if hasattr(pq, "measure_all"):
                _append(prog, pq.measure_all(qubits, cbits))
            else:
                meas = getattr(pq, "Measure", getattr(pq, "measure"))
                _append(prog, meas(qubits[0], cbits[0]))
                _append(prog, meas(qubits[1], cbits[1]))
        return machine, qubits, cbits, prog

    def _bitstring(key):
        if isinstance(key, str):
            s = "".join(ch for ch in key if ch in "01")
        elif isinstance(key, (list, tuple)):
            s = "".join("1" if bool(x) else "0" for x in key)
        else:
            s = "".join(ch for ch in str(key) if ch in "01")
        if len(s) < 2:
            s = s.zfill(2)
        elif len(s) > 2:
            s = s[-2:]
        return s

    def _dict_from_result(result):
        if result is None:
            return {}
        for attr in ("get_counts", "counts"):
            if hasattr(result, attr):
                obj = getattr(result, attr)
                result = obj() if callable(obj) else obj
                break
        if isinstance(result, dict):
            return {_bitstring(k): float(v) for k, v in result.items() if float(v) != 0.0}
        if isinstance(result, (list, tuple)):
            counts = {}
            for item in result:
                if isinstance(item, dict):
                    for k, v in item.items():
                        counts[_bitstring(k)] = counts.get(_bitstring(k), 0.0) + float(v)
                else:
                    k = _bitstring(item)
                    counts[k] = counts.get(k, 0.0) + 1.0
            return counts
        return {}

    def _normalize(counts):
        total = sum(float(v) for v in counts.values())
        if total == 0:
            return {}
        return {k: float(v) / total for k, v in counts.items() if float(v) != 0.0}

    machine, qubits, cbits, prog = _build_program(True)

    for name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
        if hasattr(machine, name):
            meth = getattr(machine, name)
            for args in ((prog, cbits, shots), (prog, shots, cbits)):
                try:
                    counts = _dict_from_result(meth(*args))
                    if counts:
                        return _normalize(counts)
                except Exception:
                    pass

    for name in ("run", "sample"):
        if hasattr(machine, name):
            meth = getattr(machine, name)
            for args in ((prog, shots), (prog, cbits, shots), (prog, shots, cbits)):
                try:
                    counts = _dict_from_result(meth(*args))
                    if counts:
                        return _normalize(counts)
                except Exception:
                    pass

    machine, qubits, cbits, prog = _build_program(False)

    for name in ("prob_run_dict", "probRunDict"):
        if hasattr(machine, name):
            meth = getattr(machine, name)
            for args in ((prog, qubits, -1), (prog, qubits)):
                try:
                    probs = _dict_from_result(meth(*args))
                    if probs:
                        return _normalize(probs)
                except Exception:
                    pass

    for name in ("prob_run_list", "probRunList"):
        if hasattr(machine, name):
            meth = getattr(machine, name)
            for args in ((prog, qubits, -1), (prog, qubits)):
                try:
                    values = list(meth(*args))
                    probs = {format(i, "02b"): float(v) for i, v in enumerate(values) if float(v) != 0.0}
                    if probs:
                        return _normalize(probs)
                except Exception:
                    pass

    for run_name in ("directly_run", "directlyRun"):
        if hasattr(machine, run_name):
            try:
                getattr(machine, run_name)(prog)
                for get_name in ("get_prob_dict", "getProbDict"):
                    if hasattr(machine, get_name):
                        probs = _dict_from_result(getattr(machine, get_name)(qubits, -1))
                        if probs:
                            return _normalize(probs)
            except Exception:
                pass

    raise RuntimeError("Unable to execute Bell circuit with pyQPanda3")
