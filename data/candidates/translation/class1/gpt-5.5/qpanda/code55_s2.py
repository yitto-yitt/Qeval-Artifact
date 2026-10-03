# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq


def or_gate(a, b):
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    def _new_machine():
        machine = pq.CPUQVM()
        for name in ("init_qvm", "init"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                    break
                except Exception:
                    pass
        return machine

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        for name in ("qAlloc", "qalloc"):
            if hasattr(machine, name):
                return [getattr(machine, name)() for _ in range(n)]
        raise RuntimeError("No qubit allocation method found")

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        for name in ("cAlloc", "calloc"):
            if hasattr(machine, name):
                return [getattr(machine, name)() for _ in range(n)]
        raise RuntimeError("No cbit allocation method found")

    def _append(prog, op):
        try:
            prog << op
        except Exception:
            if hasattr(prog, "insert"):
                prog.insert(op)
            elif hasattr(prog, "append"):
                prog.append(op)
            else:
                raise
        return prog

    def _ccx(c1, c2, target):
        for name in ("Toffoli", "TOFFOLI", "CCX", "CCNOT"):
            if hasattr(pq, name):
                gate_fn = getattr(pq, name)
                try:
                    return gate_fn(c1, c2, target)
                except Exception:
                    try:
                        return gate_fn([c1, c2], target)
                    except Exception:
                        pass
        gate = pq.X(target)
        for name in ("control", "set_control"):
            if hasattr(gate, name):
                res = getattr(gate, name)([c1, c2])
                return gate if res is None else res
        raise RuntimeError("No controlled-X construction method found")

    def _measure(q, c):
        for name in ("Measure", "measure"):
            if hasattr(pq, name):
                return getattr(pq, name)(q, c)
        raise RuntimeError("No measurement method found")

    def _build(machine):
        qubits = _alloc_qubits(machine, 9)
        qr_a = qubits[0:3]
        qr_b = qubits[3:6]
        ancillary = qubits[6:9]
        prog = pq.QProg()

        for i in range(3):
            if a_bits[2 - i] == "0":
                _append(prog, pq.X(qr_a[i]))
            if b_bits[2 - i] == "0":
                _append(prog, pq.X(qr_b[i]))

        for i in range(3):
            _append(prog, _ccx(qr_a[i], qr_b[i], ancillary[i]))

        for i in range(3):
            _append(prog, pq.X(ancillary[i]))

        return prog, ancillary

    def _bit_from_result(result):
        if isinstance(result, dict):
            key = max(result, key=lambda k: result[k])
            if isinstance(key, int):
                return "1" if key & 1 else "0"
            s = str(key)
            bits = [ch for ch in s if ch in "01"]
            return bits[-1] if bits else "0"

        if isinstance(result, (list, tuple)):
            if len(result) == 0:
                return "0"
            if all(isinstance(x, (int, float)) for x in result) and len(result) >= 2:
                return "1" if result[1] >= result[0] else "0"
            try:
                d = dict(result)
                return _bit_from_result(d)
            except Exception:
                pass

        if hasattr(result, "get_counts"):
            return _bit_from_result(result.get_counts())
        if hasattr(result, "to_dict"):
            return _bit_from_result(result.to_dict())

        s = str(result)
        bits = [ch for ch in s if ch in "01"]
        return bits[-1] if bits else "0"

    def _prob_bit(bit_index):
        machine = _new_machine()
        prog, ancillary = _build(machine)
        qlist = [ancillary[bit_index]]

        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(machine, name):
                method = getattr(machine, name)
                for args in ((prog, qlist, -1), (prog, qlist), (prog, qlist, 2)):
                    try:
                        return _bit_from_result(method(*args))
                    except Exception:
                        pass

        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(pq, name):
                method = getattr(pq, name)
                for args in ((machine, prog, qlist, -1), (prog, qlist, -1), (machine, prog, qlist), (prog, qlist)):
                    try:
                        return _bit_from_result(method(*args))
                    except Exception:
                        pass

        for run_name in ("directly_run", "run"):
            if hasattr(machine, run_name):
                try:
                    getattr(machine, run_name)(prog)
                    for pm_name in ("pmeasure_no_index", "pmeasure_bin_index", "pmeasure_dec_index", "pMeasure_no_index"):
                        if hasattr(machine, pm_name):
                            try:
                                return _bit_from_result(getattr(machine, pm_name)(qlist))
                            except Exception:
                                pass
                except Exception:
                    pass

        return _sample_bit(bit_index)

    def _run_counts(machine, prog, cbits, shots):
        for name in ("run_with_configuration", "run_with_config", "runWithConfiguration"):
            if hasattr(machine, name):
                method = getattr(machine, name)
                for args in ((prog, cbits, shots), (prog, shots, cbits)):
                    try:
                        return method(*args)
                    except Exception:
                        pass
        for name in ("run_with_configuration", "run_with_config"):
            if hasattr(pq, name):
                method = getattr(pq, name)
                for args in ((machine, prog, cbits, shots), (prog, cbits, shots)):
                    try:
                        return method(*args)
                    except Exception:
                        pass
        raise RuntimeError("No sampling execution method found")

    def _sample_bit(bit_index):
        shots = 256
        machine = _new_machine()
        prog, ancillary = _build(machine)
        cbits = _alloc_cbits(machine, 1)
        _append(prog, _measure(ancillary[bit_index], cbits[0]))
        try:
            return _bit_from_result(_run_counts(machine, prog, cbits, shots))
        except Exception:
            machine = _new_machine()
            prog, ancillary = _build(machine)
            for run_name in ("directly_run", "run"):
                if hasattr(machine, run_name):
                    try:
                        getattr(machine, run_name)(prog)
                        for qm_name in ("quick_measure", "quickMeasure"):
                            if hasattr(machine, qm_name):
                                return _bit_from_result(getattr(machine, qm_name)([ancillary[bit_index]], shots))
                    except Exception:
                        pass
        raise RuntimeError("No valid pyQPanda execution path found")

    measured_lsb = [_prob_bit(i) for i in range(3)]
    key = measured_lsb[2] + measured_lsb[1] + measured_lsb[0]
    return {key: 1.0}
