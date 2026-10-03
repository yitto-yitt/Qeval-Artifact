# EVAL_META: task_id=24, framework=qpanda, class=1
import pyqpanda3.core as pq


def dj_algorithm(oracle):
    def _num_qubits(obj):
        for name in (
            "num_qubits",
            "qubit_num",
            "qubits_num",
            "get_qubit_num",
            "get_qubits_num",
            "get_used_qubits_num",
            "get_qbit_num",
        ):
            if hasattr(obj, name):
                attr = getattr(obj, name)
                try:
                    val = attr() if callable(attr) else attr
                    if isinstance(val, int):
                        return val
                    if hasattr(val, "__len__"):
                        return len(val)
                except Exception:
                    pass
        used = _used_qubits(obj)
        if used:
            return len(used)
        raise ValueError("Unable to determine oracle qubit count")

    def _used_qubits(obj):
        for fn_name in ("get_all_used_qubits", "get_used_qubits"):
            fn = getattr(pq, fn_name, None)
            if fn is not None:
                try:
                    return list(fn(obj))
                except Exception:
                    pass
        for name in ("get_used_qubits", "used_qubits", "qubits", "get_qubits"):
            if hasattr(obj, name):
                attr = getattr(obj, name)
                try:
                    val = attr() if callable(attr) else attr
                    return list(val)
                except Exception:
                    pass
        return []

    def _init_qvm(qvm):
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(qvm, name):
                try:
                    getattr(qvm, name)()
                    return
                except Exception:
                    pass

    def _alloc_qubits(qvm, count):
        for name in ("qAlloc_many", "qAllocMany", "qalloc_many", "qallocMany", "allocate_qubits"):
            if hasattr(qvm, name):
                try:
                    return list(getattr(qvm, name)(count))
                except Exception:
                    pass
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            if hasattr(qvm, name):
                return [getattr(qvm, name)() for _ in range(count)]
        raise AttributeError("No qubit allocation method found")

    def _make_prog():
        for cls_name in ("QProg", "QCircuit"):
            cls = getattr(pq, cls_name, None)
            if cls is None:
                continue
            for args in ((), (n,)):
                try:
                    return cls(*args)
                except Exception:
                    pass
        raise AttributeError("No program/circuit class found")

    def _gate(names, qubit):
        for name in names:
            fn = getattr(pq, name, None)
            if fn is not None:
                try:
                    return fn(qubit)
                except Exception:
                    pass
        raise AttributeError("Gate constructor not found")

    def _append(container, item):
        if item is None:
            return container
        if isinstance(item, (list, tuple)):
            for sub in item:
                container = _append(container, sub)
            return container
        try:
            res = container << item
            return container if res is None else res
        except Exception:
            pass
        for name in ("insert", "append", "add", "add_gate"):
            if hasattr(container, name):
                try:
                    getattr(container, name)(item)
                    return container
                except Exception:
                    pass
        raise TypeError("Unable to append operation")

    def _oracle_on(qs):
        if callable(oracle):
            try:
                return oracle(qs)
            except TypeError:
                return oracle(*qs)
        return oracle

    def _build_program(qs):
        prog = _make_prog()
        prog = _append(prog, _gate(("X", "x"), qs[n - 1]))
        for qb in qs:
            prog = _append(prog, _gate(("H", "h"), qb))
        prog = _append(prog, _oracle_on(qs))
        for qb in qs:
            prog = _append(prog, _gate(("H", "h"), qb))
        return prog

    def _run_probs(qvm, prog, measured):
        attempts = []
        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(qvm, name):
                attempts.append((getattr(qvm, name), (prog, measured, -1)))
                attempts.append((getattr(qvm, name), (prog, measured)))
        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(pq, name):
                attempts.append((getattr(pq, name), (prog, measured, -1)))
                attempts.append((getattr(pq, name), (prog, measured)))
        for fn, args in attempts:
            try:
                return fn(*args)
            except Exception:
                pass

        for run_name in ("directly_run", "run"):
            if hasattr(qvm, run_name):
                try:
                    getattr(qvm, run_name)(prog)
                    for prob_name in ("get_prob_dict", "getProbDict", "probabilities"):
                        if hasattr(qvm, prob_name):
                            try:
                                return getattr(qvm, prob_name)(measured, -1)
                            except Exception:
                                try:
                                    return getattr(qvm, prob_name)(measured)
                                except Exception:
                                    pass
                except Exception:
                    pass

        for name in ("prob_run_dict", "probabilities", "get_prob_dict"):
            if hasattr(prog, name):
                try:
                    return getattr(prog, name)(measured, -1)
                except Exception:
                    try:
                        return getattr(prog, name)(measured)
                    except Exception:
                        pass
        raise RuntimeError("Unable to run probability simulation")

    def _normalize_result(result):
        if not isinstance(result, dict):
            try:
                result = dict(result)
            except Exception:
                result = {format(i, "0{}b".format(max(n - 1, 0))): v for i, v in enumerate(result)}
        out = {}
        width = max(n - 1, 0)
        for k, v in result.items():
            try:
                val = float(v)
            except Exception:
                continue
            if abs(val) < 1e-12:
                continue
            if isinstance(k, int):
                key = format(k, "0{}b".format(width))
            elif isinstance(k, (list, tuple)):
                key = "".join(str(int(x)) for x in k)
            else:
                key = str(k).replace(" ", "")
                if key.startswith("0b"):
                    key = format(int(key, 2), "0{}b".format(width))
            if width == 0:
                key = ""
            out[key] = out.get(key, 0.0) + val
        total = sum(out.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in out.items()}

    n = int(_num_qubits(oracle))

    last_error = None
    try:
        qvm = pq.CPUQVM()
        _init_qvm(qvm)
        qs = _alloc_qubits(qvm, n)
        prog = _build_program(qs)
        measured = list(reversed(qs[: n - 1]))
        return _normalize_result(_run_probs(qvm, prog, measured))
    except Exception as exc:
        last_error = exc

    try:
        qvm = pq.CPUQVM()
        _init_qvm(qvm)
        qs = list(range(n))
        prog = _build_program(qs)
        measured = list(reversed(qs[: n - 1]))
        return _normalize_result(_run_probs(qvm, prog, measured))
    except Exception:
        raise last_error
