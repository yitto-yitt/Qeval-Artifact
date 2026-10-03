# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq

def not_gate(a):
    def _init_machine(m):
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    return
                except Exception:
                    pass

    def _alloc(m, names, n):
        for name in names:
            if hasattr(m, name):
                try:
                    return getattr(m, name)(n)
                except Exception:
                    pass
        raise RuntimeError("allocation failed")

    def _append(prog, op):
        try:
            r = prog << op
            return prog if r is None else r
        except Exception:
            pass
        for name in ("insert", "append"):
            if hasattr(prog, name):
                r = getattr(prog, name)(op)
                return prog if r is None else r
        raise

    def _make_vec(items):
        if hasattr(pq, "QVec"):
            try:
                v = pq.QVec()
                for item in items:
                    try:
                        v.append(item)
                    except Exception:
                        v.push_back(item)
                return v
            except Exception:
                pass
        return list(items)

    def _bits_key(k):
        if isinstance(k, int):
            return format(k, "08b")
        s = str(k)
        if set(s).issubset({"0", "1"}):
            return s.zfill(8)[-8:]
        bits = "".join(ch for ch in s if ch in "01")
        if bits:
            return bits.zfill(8)[-8:]
        return s

    def _distribution(res, reverse=False):
        out = {}
        if isinstance(res, dict):
            iterable = res.items()
        elif isinstance(res, (list, tuple)):
            if len(res) == 256 and all(isinstance(x, (int, float)) for x in res):
                iterable = ((format(i, "08b"), v) for i, v in enumerate(res))
            else:
                iterable = res
        else:
            return None

        for item in iterable:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                k, v = item[0], item[1]
            else:
                continue
            key = _bits_key(k)
            if reverse:
                key = key[::-1]
            val = float(v)
            if val > 1e-12:
                out[key] = out.get(key, 0.0) + val

        total = sum(out.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in out.items()}

    machine = pq.CPUQVM()
    _init_machine(machine)

    q = _alloc(machine, ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"), 8)
    c = _alloc(machine, ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"), 8)

    prog = pq.QProg()
    a_bits = format(a, "08b")
    for i in range(8):
        if a_bits[7 - i] == "0":
            prog = _append(prog, pq.X(q[i]))

    q_order = _make_vec([q[7 - i] for i in range(8)])

    for qv, rev in ((q_order, False), (q, True)):
        if hasattr(machine, "prob_run_dict"):
            for args in ((prog, qv, -1), (prog, qv), (prog, qv, 256)):
                try:
                    dist = _distribution(machine.prob_run_dict(*args), reverse=rev)
                    if dist is not None:
                        return dist
                except Exception:
                    pass
        if hasattr(pq, "prob_run_dict"):
            for args in ((prog, qv, -1), (prog, qv), (prog, qv, 256)):
                try:
                    dist = _distribution(pq.prob_run_dict(*args), reverse=rev)
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    prog_meas = prog
    for i in range(8):
        if hasattr(pq, "Measure"):
            prog_meas = _append(prog_meas, pq.Measure(q[7 - i], c[i]))
        else:
            prog_meas = _append(prog_meas, pq.measure(q[7 - i], c[i]))

    shots = 1024
    for name in ("run_with_configuration", "run_with_config"):
        if hasattr(machine, name):
            method = getattr(machine, name)
            for args in ((prog_meas, c, shots), (prog_meas, shots, c)):
                try:
                    dist = _distribution(method(*args), reverse=False)
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    raise RuntimeError("failed to execute quantum program")
