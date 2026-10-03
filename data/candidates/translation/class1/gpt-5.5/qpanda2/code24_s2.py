# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def dj_algorithm(oracle):
    def _value(obj, names):
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        continue
                if val is not None:
                    return val
        return None

    def _as_list(x):
        if x is None:
            return []
        try:
            return list(x)
        except TypeError:
            return [x]

    def _addr(qb):
        for name in ("get_phy_addr", "get_phyaddr", "getPhysicalQubitPtr"):
            if hasattr(qb, name):
                val = getattr(qb, name)
                try:
                    val = val() if callable(val) else val
                    return int(val)
                except Exception:
                    pass
        s = str(qb)
        digits = ""
        for ch in s:
            if ch.isdigit():
                digits += ch
            elif digits:
                break
        return int(digits) if digits else 0

    def _sort_qubits(qs):
        return sorted(_as_list(qs), key=_addr)

    def _body(obj):
        for name in ("circuit", "qcircuit", "qcir", "prog", "program", "qprog"):
            if hasattr(obj, name):
                val = getattr(obj, name)
                if not callable(val) and val is not None:
                    return val
        return obj

    def _used_qubits(obj):
        for candidate in (obj, _body(obj)):
            qs = _value(candidate, ("qubits", "qvec", "qv", "used_qubits"))
            if qs is not None:
                qs = _as_list(qs)
                if qs:
                    return _sort_qubits(qs)
            for name in ("get_used_qubits", "get_qubits", "get_all_used_qubits"):
                if hasattr(candidate, name):
                    try:
                        qs = getattr(candidate, name)()
                        qs = _as_list(qs)
                        if qs:
                            return _sort_qubits(qs)
                    except Exception:
                        pass
            for fname in ("get_all_used_qubits", "get_used_qubits"):
                if hasattr(pq, fname):
                    try:
                        qs = getattr(pq, fname)(candidate)
                        qs = _as_list(qs)
                        if qs:
                            return _sort_qubits(qs)
                    except Exception:
                        pass
        return []

    def _num_qubits(obj, qs):
        val = _value(obj, ("num_qubits", "n_qubits", "qubit_num", "num_qbits"))
        if val is None:
            val = _value(_body(obj), ("num_qubits", "n_qubits", "qubit_num", "num_qbits"))
        if val is not None:
            return int(val)
        return len(qs)

    def _alloc_global(k):
        if k <= 0:
            return []
        try:
            return list(pq.qAlloc_many(k))
        except Exception:
            try:
                pq.init()
            except Exception:
                pass
            return list(pq.qAlloc_many(k))

    def _complete_qubits(qs, n):
        qs = _sort_qubits(qs)
        if len(qs) == n:
            return qs
        if len(qs) == 0:
            return _alloc_global(n)
        addrs = [_addr(qb) for qb in qs]
        max_addr = max(addrs)
        placed = {}
        ok = True
        for qb, addr in zip(qs, addrs):
            pos = n - 1 - (max_addr - addr)
            if pos < 0 or pos >= n or pos in placed:
                ok = False
                break
            placed[pos] = qb
        if not ok:
            placed = {n - len(qs) + i: qb for i, qb in enumerate(qs)}
        missing = [i for i in range(n) if i not in placed]
        new_qs = _alloc_global(len(missing))
        q = [None] * n
        for pos, qb in placed.items():
            q[pos] = qb
        for pos, qb in zip(missing, new_qs):
            q[pos] = qb
        return q

    def _append(prog, elem):
        if elem is None:
            return
        if isinstance(elem, (list, tuple)):
            for e in elem:
                _append(prog, e)
        else:
            prog << elem

    def _probabilities(prog, qvec, qvm):
        if qvm is not None and hasattr(qvm, "prob_run_dict"):
            return qvm.prob_run_dict(prog, qvec, -1)
        try:
            return pq.prob_run_dict(prog, qvec, -1)
        except Exception:
            shots = 4096
            c = qvm.cAlloc_many(len(qvec)) if qvm is not None else pq.cAlloc_many(len(qvec))
            mprog = pq.QProg()
            mprog << prog
            for i, qb in enumerate(qvec):
                mprog << pq.Measure(qb, c[i])
            if qvm is not None:
                counts = qvm.run_with_configuration(mprog, c, shots)
            else:
                counts = pq.run_with_configuration(mprog, c, shots)
            total = builtins.sum(counts.values())
            return {k: v / total for k, v in counts.items()}

    qvm = None
    if callable(oracle) and not hasattr(oracle, "__lshift__"):
        n0 = _num_qubits(oracle, [])
        qvm = pq.CPUQVM()
        qvm.init_qvm()
        q = list(qvm.qAlloc_many(n0))
        try:
            oc = oracle(q)
        except TypeError:
            try:
                oc = oracle(q, n0)
            except TypeError:
                oc = oracle(*q)
        if oc is None:
            oc = _body(oracle)
        n = n0
    else:
        oc = _body(oracle)
        qs = _used_qubits(oracle)
        n = _num_qubits(oracle, qs)
        q = _complete_qubits(qs, n)

    prog = pq.QProg()
    prog << pq.X(q[n - 1])
    for qb in q:
        prog << pq.H(qb)
    _append(prog, oc)
    for qb in q:
        prog << pq.H(qb)

    raw = _probabilities(prog, q[: n - 1], qvm)
    total = builtins.sum(float(v) for v in raw.values())
    if total == 0:
        total = 1.0

    result = {}
    width = n - 1
    for key, val in raw.items():
        p = float(val) / total
        if p <= 1e-12:
            continue
        if isinstance(key, int):
            bitstr = format(key, "0{}b".format(width))
        else:
            bitstr = "".join(ch for ch in str(key) if ch in "01")
            if len(bitstr) < width:
                bitstr = bitstr.zfill(width)
            elif len(bitstr) > width:
                bitstr = bitstr[-width:]
        result[bitstr] = result.get(bitstr, 0.0) + p

    if qvm is not None:
        qvm.finalize()

    return result
