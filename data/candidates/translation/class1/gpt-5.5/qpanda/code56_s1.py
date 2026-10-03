# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq


def not_gate(a):
    def _init_machine():
        m = pq.CPUQVM()
        for name in ("init_qvm", "init"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                except TypeError:
                    pass
                except Exception:
                    pass
        return m

    def _alloc_qubits(m, n):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        if hasattr(m, "qAlloc"):
            return [m.qAlloc() for _ in range(n)]
        if hasattr(m, "qalloc"):
            return [m.qalloc() for _ in range(n)]
        raise RuntimeError("No qubit allocation API found")

    def _alloc_cbits(m, n):
        for name in ("cAlloc_many", "calloc_many", "allocate_cbits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        if hasattr(m, "cAlloc"):
            return [m.cAlloc() for _ in range(n)]
        if hasattr(m, "calloc"):
            return [m.calloc() for _ in range(n)]
        raise RuntimeError("No cbit allocation API found")

    def _normalize_key(k, reverse=False):
        if isinstance(k, int):
            s = format(k, "08b")
        elif isinstance(k, (list, tuple)):
            s = "".join(str(int(x)) for x in k)
        else:
            s = str(k).strip().replace(" ", "")
            if s.startswith("0b"):
                s = s[2:]
            if len(s) < 8 and all(ch in "01" for ch in s):
                s = s.zfill(8)
            if len(s) > 8 and all(ch in "01" for ch in s[-8:]):
                s = s[-8:]
        if reverse:
            s = s[::-1]
        return s

    def _dist_from_raw(raw, reverse=False):
        if raw is None:
            return None
        data = {}
        if hasattr(raw, "get_counts"):
            raw = raw.get_counts()
        if isinstance(raw, dict):
            items = raw.items()
        elif hasattr(raw, "items"):
            items = raw.items()
        elif isinstance(raw, (list, tuple)):
            items = [(i, v) for i, v in enumerate(raw)]
        else:
            return None
        for k, v in items:
            try:
                val = float(v)
            except Exception:
                continue
            if val > 1e-12:
                key = _normalize_key(k, reverse)
                data[key] = data.get(key, 0.0) + val
        total = sum(data.values())
        if total == 0:
            return None
        return {k: v / total for k, v in data.items()}

    machine = _init_machine()
    q = _alloc_qubits(machine, 8)
    prog = pq.QProg()

    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            prog << pq.X(q[i])

    out_q = [q[7 - i] for i in range(8)]

    for name in ("prob_run_dict", "get_prob_dict", "pmeasure"):
        if hasattr(machine, name):
            method = getattr(machine, name)
            for args in ((prog, out_q, -1), (prog, out_q), (prog, q, -1), (prog, q)):
                try:
                    raw = method(*args)
                    dist = _dist_from_raw(raw, reverse=(args[1] is q))
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    for run_name in ("directly_run", "direct_run", "run"):
        if hasattr(machine, run_name):
            try:
                getattr(machine, run_name)(prog)
                for prob_name in ("get_prob_dict", "prob_run_dict", "pmeasure"):
                    if hasattr(machine, prob_name):
                        prob_method = getattr(machine, prob_name)
                        for args in ((out_q,), (q,)):
                            try:
                                raw = prob_method(*args)
                                dist = _dist_from_raw(raw, reverse=(args[0] is q))
                                if dist is not None:
                                    return dist
                            except Exception:
                                pass
            except Exception:
                pass

    c = _alloc_cbits(machine, 8)
    meas = getattr(pq, "Measure", None)
    if meas is None:
        meas = getattr(pq, "measure")
    for i in range(8):
        prog << meas(q[i], c[i])

    out_c = [c[7 - i] for i in range(8)]
    for name in ("run_with_configuration", "run"):
        if hasattr(machine, name):
            method = getattr(machine, name)
            for args in ((prog, out_c, 1024), (prog, c, 1024), (prog, 1024)):
                try:
                    raw = method(*args)
                    dist = _dist_from_raw(raw, reverse=(len(args) > 1 and args[1] is c))
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    raise RuntimeError("Unable to execute pyQPanda3 program")
