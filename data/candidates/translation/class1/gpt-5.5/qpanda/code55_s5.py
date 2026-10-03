# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *

def or_gate(a, b):
    def _make_machine():
        cls = getattr(pq, "CPUQVM", None) or getattr(pq, "CPUQMachine", None)
        if cls is None:
            raise RuntimeError("CPUQVM is not available")
        m = cls()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    break
                except TypeError:
                    pass
        return m

    def _alloc_many(m, names, n):
        for name in names:
            if hasattr(m, name):
                return getattr(m, name)(n)
        singular = names[-1]
        if hasattr(m, singular):
            return [getattr(m, singular)() for _ in range(n)]
        raise RuntimeError("allocation method is not available")

    def _append(prog, op):
        try:
            res = prog << op
            return prog if res is None else res
        except Exception:
            if hasattr(prog, "insert"):
                res = prog.insert(op)
                return prog if res is None else res
            raise

    def _x(q):
        return pq.X(q)

    def _ccx(c0, c1, target):
        for name in ("Toffoli", "CCX"):
            f = getattr(pq, name, None)
            if f is not None:
                return f(c0, c1, target)
        g = pq.X(target)
        if hasattr(g, "control"):
            res = g.control([c0, c1])
            return g if res is None else res
        if hasattr(g, "set_control"):
            res = g.set_control([c0, c1])
            return g if res is None else res
        raise RuntimeError("controlled-controlled-X is not available")

    def _measure(q, c):
        return pq.Measure(q, c)

    def _clean_distribution(raw, width=3):
        if raw is None:
            return None
        if not isinstance(raw, dict):
            if hasattr(raw, "get_counts"):
                raw = raw.get_counts()
            elif isinstance(raw, (list, tuple)):
                if all(isinstance(x, (int, float)) for x in raw):
                    raw = {format(i, "0{}b".format(width)): v for i, v in enumerate(raw)}
                else:
                    try:
                        raw = dict(raw)
                    except Exception:
                        return None
            else:
                return None

        out = {}
        for k, v in raw.items():
            try:
                val = float(v)
            except Exception:
                continue
            if abs(val) <= 1e-12:
                continue
            if isinstance(k, str):
                key = k.replace(" ", "")
                if len(key) > width:
                    key = key[-width:]
                elif len(key) < width:
                    key = key.zfill(width)
            else:
                key = format(int(k), "0{}b".format(width))
            out[key] = out.get(key, 0.0) + val

        total = sum(out.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in out.items()}

    def _try_prob_run(m, prog, qvec):
        calls = []
        for name in ("prob_run_dict", "probRunDict", "get_prob_dict", "getProbDict"):
            if hasattr(m, name):
                meth = getattr(m, name)
                calls.extend([(meth, (prog, qvec, -1)), (meth, (prog, qvec))])
        for name in ("prob_run_dict", "probRunDict"):
            if hasattr(pq, name):
                meth = getattr(pq, name)
                calls.extend([(meth, (prog, qvec, -1)), (meth, (prog, qvec))])
        for meth, args in calls:
            try:
                dist = _clean_distribution(meth(*args), 3)
                if dist:
                    return dist
            except Exception:
                pass
        return None

    def _try_counts_run(m, prog, cbits, shots):
        calls = []
        for name in ("run_with_configuration", "runWithConfiguration", "run_with_config", "run"):
            if hasattr(m, name):
                meth = getattr(m, name)
                calls.extend([(meth, (prog, cbits, shots)), (meth, (prog, shots)), (meth, (prog, cbits))])
        for name in ("run_with_configuration", "runWithConfiguration"):
            if hasattr(pq, name):
                meth = getattr(pq, name)
                calls.append((meth, (prog, cbits, shots)))
        for meth, args in calls:
            try:
                dist = _clean_distribution(meth(*args), 3)
                if dist:
                    return dist
            except Exception:
                pass
        raise RuntimeError("unable to execute quantum program")

    machine = _make_machine()
    qr_a = _alloc_many(machine, ("qAlloc_many", "qalloc_many", "q_alloc_many", "qAlloc"), 3)
    qr_b = _alloc_many(machine, ("qAlloc_many", "qalloc_many", "q_alloc_many", "qAlloc"), 3)
    ancillary = _alloc_many(machine, ("qAlloc_many", "qalloc_many", "q_alloc_many", "qAlloc"), 3)

    prog = pq.QProg()
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "0":
            prog = _append(prog, _x(qr_a[i]))
        if b_bits[2 - i] == "0":
            prog = _append(prog, _x(qr_b[i]))

    for i in range(3):
        prog = _append(prog, _ccx(qr_a[i], qr_b[i], ancillary[i]))

    for i in range(3):
        prog = _append(prog, _x(ancillary[i]))

    prob_dist = _try_prob_run(machine, prog, [ancillary[2], ancillary[1], ancillary[0]])
    if prob_dist is not None:
        return prob_dist

    cbits = _alloc_many(machine, ("cAlloc_many", "calloc_many", "c_alloc_many", "cAlloc"), 3)
    prog = _append(prog, _measure(ancillary[2], cbits[0]))
    prog = _append(prog, _measure(ancillary[1], cbits[1]))
    prog = _append(prog, _measure(ancillary[0], cbits[2]))
    return _try_counts_run(machine, prog, cbits, 1024)
