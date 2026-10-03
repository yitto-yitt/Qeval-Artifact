# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    shots = int(samples)

    def _init_qvm(qvm):
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    method()
                    return
                except TypeError:
                    pass

    def _to_list(obj, n):
        try:
            return list(obj)
        except Exception:
            return [obj[i] for i in range(n)]

    def _alloc(qvm, many_names, one_names, n):
        for name in many_names:
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    return _to_list(method(n), n)
                except Exception:
                    pass
        for name in one_names:
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    return [method() for _ in range(n)]
                except Exception:
                    pass
        return None

    def _append(prog, op):
        try:
            new_prog = prog.__lshift__(op)
            return prog if new_prog is None else new_prog
        except Exception:
            pass
        for name in ("insert", "append", "push_back"):
            method = getattr(prog, name, None)
            if callable(method):
                try:
                    method(op)
                    return prog
                except Exception:
                    pass
        raise RuntimeError("Unable to append operation to pyQPanda3 program")

    def _new_prog():
        cls = getattr(pq, "QProg", None) or getattr(pq, "QCircuit", None)
        if cls is None:
            raise RuntimeError("No pyQPanda3 program class found")
        for args in ((), (1,)):
            try:
                return cls(*args)
            except Exception:
                pass
        raise RuntimeError("Unable to construct pyQPanda3 program")

    def _measure_op(q, c):
        for name in ("Measure", "measure"):
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    return fn(q, c)
                except Exception:
                    pass
        raise RuntimeError("No pyQPanda3 measurement operation found")

    def _make_program(measured):
        qvm_cls = getattr(pq, "CPUQVM", None)
        if qvm_cls is None:
            raise RuntimeError("No CPUQVM class found in pyQPanda3")
        qvm = qvm_cls()
        _init_qvm(qvm)

        qubits = _alloc(
            qvm,
            ("qAlloc_many", "qalloc_many", "allocate_qubits", "alloc_qubits"),
            ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"),
            1,
        )
        cbits = _alloc(
            qvm,
            ("cAlloc_many", "calloc_many", "allocate_cbits", "alloc_cbits"),
            ("cAlloc", "calloc", "allocate_cbit", "alloc_cbit"),
            1,
        )

        if qubits is None:
            qubits = [0]
        if cbits is None:
            cbits = [0]

        prog = _new_prog()
        prog = _append(prog, pq.H(qubits[0]))
        if measured:
            prog = _append(prog, _measure_op(qubits[0], cbits[0]))
        return qvm, prog, qubits, cbits

    def _bit_from_key(key):
        if isinstance(key, (list, tuple)) and len(key) == 1:
            key = key[0]
        if isinstance(key, bool):
            return "1" if key else "0"
        if isinstance(key, int):
            return "1" if key & 1 else "0"
        s = str(key)
        bits = [ch for ch in s if ch in "01"]
        if not bits:
            return None
        return bits[-1]

    def _counts_to_distribution(counts):
        heads = 0.0
        tails = 0.0
        for key, value in counts.items():
            bit = _bit_from_key(key)
            if bit == "0":
                heads += float(value)
            elif bit == "1":
                tails += float(value)
        total = heads + tails
        if total <= 0:
            raise RuntimeError("No measurement results produced")
        return {"Heads": heads / total, "Tails": tails / total}

    def _result_to_counts(result):
        if result is None:
            raise RuntimeError("Empty result")
        for name in ("get_counts", "get_measure_result", "get_result"):
            method = getattr(result, name, None)
            if callable(method):
                try:
                    return _result_to_counts(method())
                except Exception:
                    pass
        if isinstance(result, dict):
            return result
        try:
            converted = dict(result)
            if converted:
                return converted
        except Exception:
            pass
        if isinstance(result, (list, tuple)):
            counts = {}
            for item in result:
                bit = _bit_from_key(item)
                if bit is not None:
                    counts[bit] = counts.get(bit, 0) + 1
            if counts:
                return counts
        raise RuntimeError("Unsupported result format")

    def _try_sampling_run(qvm, prog, qubits, cbits):
        call_specs = []
        for owner in (qvm, pq):
            for name in ("run_with_configuration", "run"):
                method = getattr(owner, name, None)
                if callable(method):
                    call_specs.extend((
                        (method, (prog, cbits, shots), {}),
                        (method, (prog, shots), {}),
                        (method, (prog,), {"shots": shots}),
                    ))
        for method, args, kwargs in call_specs:
            try:
                return _counts_to_distribution(_result_to_counts(method(*args, **kwargs)))
            except Exception:
                pass
        return None

    try:
        qvm, prog, qubits, cbits = _make_program(True)
        dist = _try_sampling_run(qvm, prog, qubits, cbits)
        if dist is not None:
            return dist
    except Exception:
        pass

    qvm, prog, qubits, cbits = _make_program(False)

    for direct_name in ("directly_run", "direct_run", "run"):
        direct = getattr(qvm, direct_name, None)
        if callable(direct):
            try:
                direct(prog)
                for qm_name in ("quick_measure", "quickMeasure"):
                    qm = getattr(qvm, qm_name, None)
                    if callable(qm):
                        return _counts_to_distribution(_result_to_counts(qm(qubits, shots)))
            except Exception:
                pass

    for name in ("prob_run_dict", "probRunDict"):
        method = getattr(qvm, name, None)
        if callable(method):
            for args in ((prog, qubits, -1), (prog, qubits), (prog,)):
                try:
                    return _counts_to_distribution(_result_to_counts(method(*args)))
                except Exception:
                    pass

    dist = _try_sampling_run(qvm, prog, qubits, cbits)
    if dist is not None:
        return dist

    raise RuntimeError("Unable to execute pyQPanda3 quantum coin flip")
