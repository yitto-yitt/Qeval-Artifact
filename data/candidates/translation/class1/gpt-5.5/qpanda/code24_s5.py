# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *
import math

def dj_algorithm(oracle):
    def _call_attr(obj, names):
        for name in names:
            if hasattr(obj, name):
                v = getattr(obj, name)
                try:
                    return v() if callable(v) else v
                except TypeError:
                    pass
        return None

    def _qid(q):
        for name in ("get_phy_addr", "getPhysicalQubitPtr", "get_addr", "get_index", "get_id", "id"):
            if hasattr(q, name):
                v = getattr(q, name)
                try:
                    v = v() if callable(v) else v
                    return int(v)
                except Exception:
                    pass
        for name in ("phy_addr", "addr", "index"):
            if hasattr(q, name):
                try:
                    return int(getattr(q, name))
                except Exception:
                    pass
        try:
            return int(q)
        except Exception:
            return None

    def _unique_sorted(qs):
        out = []
        seen = set()
        for q in qs:
            k = _qid(q)
            k = ("id", id(q)) if k is None else ("addr", k)
            if k not in seen:
                seen.add(k)
                out.append(q)
        return sorted(out, key=lambda x: (_qid(x) is None, _qid(x) if _qid(x) is not None else id(x)))

    def _append(container, item):
        try:
            container << item
            return container
        except Exception:
            pass
        try:
            container.insert(item)
            return container
        except Exception:
            pass
        try:
            return container.append(item)
        except Exception:
            pass
        raise

    def _init_machine(m):
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    return
                except Exception:
                    pass

    def _alloc_many(m, k):
        for name in ("qAlloc_many", "qAllocMany", "qalloc_many", "allocate_qubits"):
            if hasattr(m, name):
                try:
                    return list(getattr(m, name)(k))
                except Exception:
                    pass
        qs = []
        for _ in range(k):
            for name in ("qAlloc", "qalloc", "allocate_qubit"):
                if hasattr(m, name):
                    try:
                        qs.append(getattr(m, name)())
                        break
                    except Exception:
                        pass
        return qs

    def _run(machine, program):
        for name in ("directly_run", "run", "run_qprog", "execute"):
            if hasattr(machine, name):
                try:
                    return getattr(machine, name)(program)
                except Exception:
                    pass
        if "directly_run" in globals():
            try:
                return directly_run(program)
            except Exception:
                pass
        if "run" in globals():
            try:
                return run(program)
            except Exception:
                pass
        return None

    def _state(machine):
        for name in ("get_qstate", "get_qstate_vector", "getQState", "get_qstate_all"):
            if hasattr(machine, name):
                try:
                    return list(getattr(machine, name)())
                except Exception:
                    pass
        return None

    def _little_endian():
        try:
            cm = CPUQVM()
            _init_machine(cm)
            cq = _alloc_many(cm, 2)
            cp = QProg()
            _append(cp, X(cq[0]))
            _run(cm, cp)
            st = _state(cm)
            if st:
                idx = max(range(len(st)), key=lambda i: abs(st[i]) ** 2)
                return idx == 1
        except Exception:
            pass
        return True

    def _prob_fallback(machine, program, measured):
        qsel = list(reversed(measured))
        attempts = []
        for name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list"):
            if hasattr(machine, name):
                attempts.append(getattr(machine, name))
        for name in ("prob_run_dict", "probRunDict"):
            if name in globals():
                attempts.append(globals()[name])
        for fn in attempts:
            for args in ((program, qsel, -1), (program, qsel), (program, measured, -1), (program, measured)):
                try:
                    r = fn(*args)
                    if isinstance(r, dict):
                        total = float(sum(r.values()))
                        if total == 0:
                            continue
                        return {str(k): float(v) / total for k, v in r.items() if float(v) != 0.0}
                    if isinstance(r, (list, tuple)):
                        d = {}
                        for item in r:
                            if isinstance(item, (list, tuple)) and len(item) >= 2:
                                d[str(item[0])] = float(item[1])
                        total = float(sum(d.values()))
                        if total:
                            return {k: v / total for k, v in d.items() if v != 0.0}
                except Exception:
                    pass
        return None

    n = _call_attr(oracle, ("num_qubits", "qubit_count", "get_qubit_count", "get_qubits_num"))
    if n is not None:
        n = int(n)

    qubits = None
    for names in (("get_used_qubits",), ("used_qubits",), ("get_qubits",), ("qubits",), ("qbits",)):
        qs = _call_attr(oracle, names)
        if qs is not None:
            try:
                qubits = _unique_sorted(list(qs))
                break
            except Exception:
                pass
    if qubits is None:
        for fname in ("get_all_used_qubits", "get_used_qubits"):
            if fname in globals():
                try:
                    qubits = _unique_sorted(list(globals()[fname](oracle)))
                    break
                except Exception:
                    pass

    qvm = CPUQVM()
    _init_machine(qvm)

    if qubits:
        if n is None:
            n = len(qubits)
        max_addr = max([_qid(q) for q in qubits if _qid(q) is not None] or [n - 1])
        _alloc_many(qvm, max(max_addr + 1, n))
        qubits = qubits[:n]
    else:
        qubits = _alloc_many(qvm, n)

    prog = QProg()
    _append(prog, X(qubits[n - 1]))
    for q in qubits:
        _append(prog, H(q))

    try:
        _append(prog, oracle)
    except Exception:
        _append(prog, oracle(qubits))

    for q in qubits:
        _append(prog, H(q))

    input_qubits = list(qubits[:n - 1])
    _run(qvm, prog)
    state = _state(qvm)

    if state:
        little = _little_endian()
        m = int(round(math.log(len(state), 2))) if len(state) > 1 else 0
        sorted_all = _unique_sorted(qubits)
        compact_index = {id(q): i for i, q in enumerate(sorted_all)}
        probs = {}
        for idx, amp in enumerate(state):
            p = abs(amp) ** 2
            if p <= 1e-12:
                continue
            bits = []
            for q in reversed(input_qubits):
                a = _qid(q)
                if a is None or a < 0 or a >= m:
                    a = compact_index.get(id(q), 0)
                pos = a if little else (m - 1 - a)
                bits.append("1" if ((idx >> pos) & 1) else "0")
            key = "".join(bits)
            probs[key] = probs.get(key, 0.0) + float(p)
        total = sum(probs.values())
        if total:
            return {k: v / total for k, v in probs.items() if v > 1e-12}

    fb = _prob_fallback(qvm, prog, input_qubits)
    if fb is not None:
        return fb
    return {"": 1.0} if n == 1 else {}
