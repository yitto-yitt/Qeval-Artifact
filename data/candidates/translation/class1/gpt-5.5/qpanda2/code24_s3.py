# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def dj_algorithm(oracle):
    machine = None

    def _maybe_call(x):
        try:
            return x()
        except TypeError:
            return x

    def _num_qubits(obj):
        for name in ("num_qubits", "n_qubits", "qubit_num", "qubits_num"):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    v = v() if callable(v) else v
                    return int(v)
                except Exception:
                    pass
        return None

    def _as_list(v):
        if v is None:
            return None
        try:
            return list(v)
        except Exception:
            try:
                return [v[i] for i in range(len(v))]
            except Exception:
                return None

    def _attr_qubits(obj):
        for name in ("qubits", "qvec", "qv", "qs", "q"):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    v = v() if callable(v) else v
                    lst = _as_list(v)
                    if lst is not None:
                        return lst
                except Exception:
                    pass
        for name in ("get_qubits", "get_qvec", "get_qv"):
            if hasattr(obj, name):
                try:
                    lst = _as_list(getattr(obj, name)())
                    if lst is not None:
                        return lst
                except Exception:
                    pass
        return None

    def _circuit_obj(obj):
        for name in ("circuit", "circ", "prog", "program", "oracle"):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    return v() if callable(v) else v
                except Exception:
                    pass
        return obj

    def _used_qubits(obj):
        qs = _attr_qubits(obj)
        if qs is not None:
            return qs
        target = _circuit_obj(obj)
        for fname in ("get_all_used_qubits", "get_used_qubits", "get_qprog_used_qubits"):
            f = getattr(pq, fname, None)
            if f is not None:
                try:
                    qs = _as_list(f(target))
                    if qs is not None:
                        return qs
                except Exception:
                    pass
                try:
                    tmp = pq.QProg()
                    tmp << target
                    qs = _as_list(f(tmp))
                    if qs is not None:
                        return qs
                except Exception:
                    pass
        for mname in ("get_used_qubits", "get_all_used_qubits"):
            if hasattr(target, mname):
                try:
                    qs = _as_list(getattr(target, mname)())
                    if qs is not None:
                        return qs
                except Exception:
                    pass
        return []

    def _addr(qb):
        for fname in ("get_phy_addr", "get_physical_addr", "get_qubit_addr"):
            f = getattr(pq, fname, None)
            if f is not None:
                try:
                    return int(f(qb))
                except Exception:
                    pass
        for mname in ("get_phy_addr", "getPhysicalQubitPtr", "get_phyaddr", "get_addr"):
            if hasattr(qb, mname):
                try:
                    v = getattr(qb, mname)()
                    return int(v)
                except Exception:
                    pass
        return None

    def _sort_qubits(qs):
        indexed = []
        ok = True
        for i, qb in enumerate(qs):
            a = _addr(qb)
            if a is None:
                ok = False
            indexed.append((a, i, qb))
        if ok:
            indexed.sort(key=lambda t: t[0])
        else:
            indexed.sort(key=lambda t: t[1])
        return [t[2] for t in indexed]

    def _alloc_qubits(k):
        nonlocal machine
        if k <= 0:
            return []
        if machine is not None:
            return list(machine.qAlloc_many(k))
        try:
            return list(pq.qAlloc_many(k))
        except Exception:
            machine = pq.init_quantum_machine(pq.QMachineType.CPU)
            return list(pq.qAlloc_many(k))

    def _alloc_cbits(k):
        nonlocal machine
        if k <= 0:
            return []
        if machine is not None:
            return list(machine.cAlloc_many(k))
        try:
            return list(pq.cAlloc_many(k))
        except Exception:
            machine = pq.init_quantum_machine(pq.QMachineType.CPU)
            return list(pq.cAlloc_many(k))

    if hasattr(oracle, "machine"):
        try:
            machine = getattr(oracle, "machine")
        except Exception:
            machine = None
    if machine is None and hasattr(oracle, "qvm"):
        try:
            machine = getattr(oracle, "qvm")
        except Exception:
            machine = None

    if isinstance(oracle, (tuple, list)) and len(oracle) >= 1:
        circ = oracle[0]
        qvec = _as_list(oracle[1]) if len(oracle) >= 2 else None
        n = int(oracle[2]) if len(oracle) >= 3 else _num_qubits(circ)
    else:
        circ = _circuit_obj(oracle)
        qvec = _attr_qubits(oracle)
        n = _num_qubits(oracle)
        if n is None:
            n = _num_qubits(circ)

    if callable(circ) and n is not None:
        qvec = _alloc_qubits(n)
        try:
            built = circ(qvec)
        except TypeError:
            try:
                built = circ(qvec, n)
            except TypeError:
                built = circ()
        if built is not None:
            circ = built

    if qvec is None:
        qvec = _used_qubits(circ)
    if qvec is None:
        qvec = []

    qvec = _sort_qubits(qvec)

    if n is None:
        n = len(qvec)

    if len(qvec) < n:
        placed = [None] * n
        used = _sort_qubits(qvec)
        addrs = [_addr(qb) for qb in used]
        used_positions = None
        if addrs and all(a is not None for a in addrs):
            base = min(addrs)
            cand = [a - base for a in addrs]
            if all(0 <= p < n for p in cand) and len(set(cand)) == len(cand):
                used_positions = cand
        if used_positions is None:
            if len(used) == 1:
                used_positions = [n - 1]
            else:
                used_positions = list(range(len(used)))
        for qb, pos in zip(used, used_positions):
            if 0 <= pos < n and placed[pos] is None:
                placed[pos] = qb
        missing = builtins.sum(1 for x in placed if x is None)
        new_qs = _alloc_qubits(missing)
        it = iter(new_qs)
        for i in range(n):
            if placed[i] is None:
                placed[i] = next(it)
        qvec = placed
    elif len(qvec) > n:
        qvec = qvec[:n]

    prog = pq.QProg()
    prog << pq.X(qvec[n - 1])
    for qb in qvec:
        prog << pq.H(qb)
    if circ is not None:
        prog << circ
    for qb in qvec:
        prog << pq.H(qb)

    input_qubits = list(reversed(qvec[:n - 1]))

    if n - 1 == 0:
        return {"": 1.0}

    try:
        if machine is not None and hasattr(machine, "prob_run_dict"):
            probs = machine.prob_run_dict(prog, input_qubits, -1)
        else:
            probs = pq.prob_run_dict(prog, input_qubits, -1)
        dist = {}
        for k, v in dict(probs).items():
            p = float(v)
            if p > 1e-12:
                key = str(k)
                if len(key) < n - 1:
                    key = key.zfill(n - 1)
                dist[key] = dist.get(key, 0.0) + p
        total = builtins.sum(dist.values())
        if total != 0:
            return {k: v / total for k, v in dist.items()}
    except Exception:
        pass

    cbits = _alloc_cbits(n - 1)
    meas_prog = pq.QProg()
    meas_prog << prog
    for i, qb in enumerate(input_qubits):
        meas_prog << pq.Measure(qb, cbits[i])

    shots = 4096
    if machine is not None and hasattr(machine, "run_with_configuration"):
        counts = machine.run_with_configuration(meas_prog, cbits, shots)
    else:
        counts = pq.run_with_configuration(meas_prog, cbits, shots)

    total = builtins.sum(counts.values())
    return {str(key).zfill(n - 1): value / total for key, value in counts.items() if value}
