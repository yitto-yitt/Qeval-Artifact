# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq


def xor_gate(a, b):
    shots = 1024

    def _new_qvm():
        cls = None
        for name in ("CPUQVM", "CpuQVM", "CPUSingleThreadQVM"):
            cls = getattr(pq, name, None)
            if cls is not None:
                break
        if cls is None:
            raise RuntimeError("No CPU quantum virtual machine found in pyqpanda3.core")
        qvm = cls()
        if hasattr(qvm, "set_configure"):
            try:
                qvm.set_configure(8, 8)
            except Exception:
                pass
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(qvm, name, None)
            if method is not None:
                try:
                    method()
                    break
                except TypeError:
                    try:
                        method(8, 8)
                        break
                    except Exception:
                        pass
                except Exception:
                    pass
        return qvm

    def _alloc_many(qvm, n, quantum):
        if quantum:
            many_names = ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany")
            one_names = ("qAlloc", "qalloc", "allocate_qubit")
        else:
            many_names = ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany")
            one_names = ("cAlloc", "calloc", "allocate_cbit")
        for name in many_names:
            method = getattr(qvm, name, None)
            if method is not None:
                try:
                    return method(n)
                except Exception:
                    pass
        for name in one_names:
            method = getattr(qvm, name, None)
            if method is not None:
                return [method() for _ in range(n)]
        raise RuntimeError("Allocation method not found")

    def _append(prog, op):
        try:
            result = prog << op
            return prog if result is None else result
        except Exception:
            method = getattr(prog, "insert", None)
            if method is not None:
                result = method(op)
                return prog if result is None else result
            raise

    def _measure_all(prog, q, c):
        func = getattr(pq, "measure_all", None)
        if func is not None:
            try:
                return _append(prog, func(q, c))
            except Exception:
                pass
        func = getattr(pq, "Measure", None) or getattr(pq, "measure", None)
        if func is None:
            raise RuntimeError("Measurement function not found")
        for i in range(8):
            prog = _append(prog, func(q[i], c[i]))
        return prog

    def _make_program(bits_to_flip, measured):
        qvm = _new_qvm()
        q = _alloc_many(qvm, 8, True)
        c = _alloc_many(qvm, 8, False) if measured else None
        prog = pq.QProg()
        x_gate = getattr(pq, "X", None) or getattr(pq, "x", None)
        if x_gate is None:
            raise RuntimeError("X gate not found")
        for idx in bits_to_flip:
            prog = _append(prog, x_gate(q[idx]))
        if measured:
            prog = _measure_all(prog, q, c)
        return qvm, q, c, prog

    def _to_dict(result):
        if isinstance(result, dict):
            return result
        get_counts = getattr(result, "get_counts", None)
        if get_counts is not None:
            return get_counts()
        try:
            return dict(result)
        except Exception:
            pass
        items = getattr(result, "items", None)
        if items is not None:
            return dict(items())
        raise RuntimeError("Unsupported result type")

    def _run_measured(qvm, prog, c):
        for name in ("run_with_configuration", "runWithConfiguration"):
            method = getattr(qvm, name, None)
            if method is not None:
                for args in ((prog, c, shots), (prog, shots), (prog,)):
                    try:
                        result = method(*args)
                        if result is not None:
                            return _to_dict(result)
                    except Exception:
                        pass
        for name in ("run_with_configuration", "runWithConfiguration"):
            func = getattr(pq, name, None)
            if func is not None:
                for args in ((prog, c, shots), (prog, shots), (prog,)):
                    try:
                        result = func(*args)
                        if result is not None:
                            return _to_dict(result)
                    except Exception:
                        pass
        raise RuntimeError("Measured execution failed")

    def _run_prob(qvm, prog, q):
        for name in ("prob_run_dict", "probRunDict", "get_prob_dict", "prob_run_tuple_list"):
            method = getattr(qvm, name, None)
            if method is not None:
                for args in ((prog, q, -1), (prog, q), (prog,)):
                    try:
                        result = method(*args)
                        if result is not None:
                            return _to_dict(result)
                    except Exception:
                        pass
        for name in ("prob_run_dict", "probRunDict"):
            func = getattr(pq, name, None)
            if func is not None:
                for args in ((prog, q, -1), (prog, q), (prog,)):
                    try:
                        result = func(*args)
                        if result is not None:
                            return _to_dict(result)
                    except Exception:
                        pass
        raise RuntimeError("Probability execution failed")

    def _execute(bits_to_flip):
        try:
            qvm, q, c, prog = _make_program(bits_to_flip, True)
            return _run_measured(qvm, prog, c)
        except Exception:
            qvm, q, c, prog = _make_program(bits_to_flip, False)
            return _run_prob(qvm, prog, q)

    def _clean_key(key):
        if isinstance(key, int):
            s = format(key, "08b")
        else:
            s = "".join(ch for ch in str(key) if ch in "01")
            if len(s) < 8:
                s = s.zfill(8)
            elif len(s) > 8:
                s = s[-8:]
        return s

    mapping = getattr(xor_gate, "_bit_mapping", None)
    if mapping is None:
        mapping = {}
        for qubit_index in range(8):
            counts = _execute([qubit_index])
            key = max(counts, key=lambda k: float(counts[k]))
            s = _clean_key(key)
            ones = [i for i, ch in enumerate(s) if ch == "1"]
            if len(ones) != 1:
                mapping = {i: i for i in range(8)}
                break
            mapping[ones[0]] = 7 - qubit_index
        if len(mapping) != 8:
            mapping = {i: i for i in range(8)}
        xor_gate._bit_mapping = mapping

    flips = []
    a = int(a)
    b = int(b)
    for value in (a, b):
        for i in range(8):
            if (value >> i) & 1:
                flips.append(i)

    raw_counts = _execute(flips)
    transformed = {}
    for key, value in raw_counts.items():
        s = _clean_key(key)
        out = ["0"] * 8
        for raw_index, ch in enumerate(s):
            if raw_index in mapping:
                out[mapping[raw_index]] = ch
        out_key = "".join(out)
        v = float(value)
        if v != 0.0:
            transformed[out_key] = transformed.get(out_key, 0.0) + v

    total = sum(transformed.values())
    return {key: value / total for key, value in transformed.items()}
