# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def dj_algorithm(oracle):
    def _addr(q):
        try:
            a = q.get_phy_addr
            return a() if callable(a) else a
        except Exception:
            try:
                return int(q)
            except Exception:
                return 0

    def _alloc_qubits(k):
        try:
            return list(pq.qAlloc_many(k))
        except Exception:
            pq.init()
            return list(pq.qAlloc_many(k))

    def _alloc_cbits(k):
        try:
            return list(pq.cAlloc_many(k))
        except Exception:
            pq.init()
            return list(pq.cAlloc_many(k))

    def _num_qubits(obj):
        for name in ("num_qubits", "qubit_num", "n_qubits", "n"):
            if hasattr(obj, name):
                v = getattr(obj, name)
                try:
                    v = v() if callable(v) else v
                    if isinstance(v, int):
                        return v
                except Exception:
                    pass
        return None

    def _used_qubits(obj):
        for name in ("qubits", "qbits", "qvec"):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    v = v() if callable(v) else v
                    qs = list(v)
                    if qs:
                        return qs
                except Exception:
                    pass
        try:
            qs = list(pq.get_all_used_qubits(obj))
            if qs:
                return sorted(qs, key=_addr)
        except Exception:
            pass
        try:
            p = pq.QProg()
            p.insert(obj)
            qs = list(pq.get_all_used_qubits(p))
            if qs:
                return sorted(qs, key=_addr)
        except Exception:
            pass
        return []

    if callable(oracle) and not hasattr(oracle, "insert"):
        n = _num_qubits(oracle)
        qubits = _alloc_qubits(n)
        built_oracle = oracle(qubits)
        if built_oracle is None:
            built_oracle = oracle
    else:
        built_oracle = oracle
        qubits = _used_qubits(built_oracle)
        n = _num_qubits(built_oracle)
        if n is None:
            n = len(qubits)
        if not qubits:
            qubits = _alloc_qubits(n)
            if callable(oracle):
                built_oracle = oracle(qubits)

    qubits = list(qubits)
    n = int(n)

    prog = pq.QProg()
    prog.insert(pq.X(qubits[n - 1]))
    for q in qubits:
        prog.insert(pq.H(q))
    prog.insert(built_oracle)
    for q in qubits:
        prog.insert(pq.H(q))

    input_qubits = qubits[: n - 1]

    if n - 1 == 0:
        try:
            pq.directly_run(prog)
        except Exception:
            try:
                pq.prob_run_dict(prog, [qubits[n - 1]], -1)
            except Exception:
                pass
        return {"": 1.0}

    def _prob_first_char_is_first_qubit():
        a, b = _alloc_qubits(2)
        p = pq.QProg()
        p.insert(pq.X(a))
        try:
            d = pq.prob_run_dict(p, [a, b], -1)
        except TypeError:
            d = pq.prob_run_dict(p, [a, b])
        mk = max(d, key=d.get)
        return str(mk).zfill(2)[-2:] == "10"

    try:
        first_is_first = _prob_first_char_is_first_qubit()
    except Exception:
        first_is_first = True

    try:
        try:
            probs = pq.prob_run_dict(prog, input_qubits, -1)
        except TypeError:
            probs = pq.prob_run_dict(prog, input_qubits)

        result = {}
        width = n - 1
        for key, value in probs.items():
            pval = float(value)
            if pval <= 1e-12:
                continue
            if isinstance(key, int):
                skey = format(key, "0{}b".format(width))
            else:
                skey = str(key)
                if skey.startswith("0b"):
                    skey = format(int(skey, 2), "0{}b".format(width))
                elif len(skey) < width:
                    skey = skey.zfill(width)
                elif len(skey) > width:
                    skey = skey[-width:]
            qiskit_key = skey[::-1] if first_is_first else skey
            result[qiskit_key] = result.get(qiskit_key, 0.0) + pval

        total = builtins.sum(result.values())
        return {k: v / total for k, v in result.items() if v > 1e-12}

    except Exception:
        cbits = _alloc_cbits(n - 1)
        meas_prog = pq.QProg()
        meas_prog.insert(prog)
        for i in range(n - 1):
            meas_prog.insert(pq.Measure(input_qubits[i], cbits[i]))
        shots = 8192
        counts = pq.run_with_configuration(meas_prog, cbits, shots)
        total = builtins.sum(counts.values())
        return {str(k): v / total for k, v in counts.items() if v > 0}
