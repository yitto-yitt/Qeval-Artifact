# EVAL_META: task_id=1, framework=qpanda, class=1
import pyqpanda3.core as pq
from numbers import Number

def run_bell_state_simulator():
    shots = 1000

    def _call(fn, *args):
        try:
            return fn(*args)
        except Exception:
            return None

    def _normalize(result, width=2):
        if result is None:
            return None

        def key_to_bits(key):
            if isinstance(key, str):
                s = "".join(ch for ch in key if ch in "01")
                if not s:
                    return None
                return s[-width:].zfill(width)
            if isinstance(key, int):
                return format(key, "0{}b".format(width))[-width:]
            if isinstance(key, (tuple, list)):
                try:
                    return "".join("1" if int(x) else "0" for x in key)[-width:].zfill(width)
                except Exception:
                    return None
            return None

        items = None
        if isinstance(result, dict):
            items = list(result.items())
        else:
            try:
                seq = list(result)
            except Exception:
                return None

            if all(isinstance(x, str) for x in seq):
                counts = {}
                for x in seq:
                    b = key_to_bits(x)
                    if b is not None:
                        counts[b] = counts.get(b, 0.0) + 1.0
                items = list(counts.items())
            elif all(isinstance(x, Number) and not isinstance(x, complex) for x in seq):
                items = [(i, v) for i, v in enumerate(seq)]
            else:
                pairs = []
                for x in seq:
                    try:
                        if len(x) >= 2:
                            pairs.append((x[0], x[1]))
                    except Exception:
                        pass
                items = pairs

        probs = {}
        for k, v in items:
            b = key_to_bits(k)
            if b is None:
                continue
            try:
                val = float(v)
            except Exception:
                continue
            if val > 1e-15:
                probs[b] = probs.get(b, 0.0) + val

        total = sum(probs.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in probs.items()}

    def _state_to_probs(state, width=2):
        try:
            seq = list(state)
        except Exception:
            return None
        if len(seq) < 2:
            return None
        probs = {}
        for i, amp in enumerate(seq):
            try:
                p = abs(complex(amp)) ** 2
            except Exception:
                continue
            if p > 1e-15:
                probs[format(i, "0{}b".format(width))[-width:]] = probs.get(format(i, "0{}b".format(width))[-width:], 0.0) + p
        total = sum(probs.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in probs.items()}

    def _make_machine():
        qvm = None
        cls = getattr(pq, "CPUQVM", None)
        if cls is not None:
            qvm = _call(cls)
        if qvm is None and hasattr(pq, "init_quantum_machine"):
            qmt = getattr(pq, "QMachineType", None)
            candidates = []
            if qmt is not None:
                for name in ("CPU", "CPU_SINGLE_THREAD", "CPUQVM"):
                    if hasattr(qmt, name):
                        candidates.append(getattr(qmt, name))
            candidates.append(None)
            for cand in candidates:
                qvm = _call(pq.init_quantum_machine, cand) if cand is not None else _call(pq.init_quantum_machine)
                if qvm is not None:
                    break
        if qvm is not None:
            for name in ("init_qvm", "initQVM", "init"):
                fn = getattr(qvm, name, None)
                if fn is not None:
                    _call(fn)
                    break
        return qvm

    def _alloc_many(owner, n, many_names, one_names):
        if owner is not None:
            for name in many_names:
                fn = getattr(owner, name, None)
                if fn is not None:
                    r = _call(fn, n)
                    if r is not None:
                        return r
            for name in one_names:
                fn = getattr(owner, name, None)
                if fn is not None:
                    out = []
                    ok = True
                    for _ in range(n):
                        x = _call(fn)
                        if x is None:
                            ok = False
                            break
                        out.append(x)
                    if ok:
                        return out
        for name in many_names:
            fn = getattr(pq, name, None)
            if fn is not None:
                r = _call(fn, n)
                if r is not None:
                    return r
        for name in one_names:
            fn = getattr(pq, name, None)
            if fn is not None:
                out = []
                ok = True
                for _ in range(n):
                    x = _call(fn)
                    if x is None:
                        ok = False
                        break
                    out.append(x)
                if ok:
                    return out
        return list(range(n))

    def _new_prog():
        for cls_name in ("QProg", "QCircuit"):
            cls = getattr(pq, cls_name, None)
            if cls is None:
                continue
            for args in ((), (2,)):
                prog = _call(cls, *args)
                if prog is not None:
                    return prog
        raise RuntimeError("Unable to construct pyQPanda3 quantum program")

    def _append(prog, op):
        if op is None:
            return prog
        if isinstance(op, (list, tuple)):
            for item in op:
                prog = _append(prog, item)
            return prog
        try:
            r = prog << op
            return r if r is not None else prog
        except Exception:
            pass
        for name in ("insert", "push_back", "append"):
            fn = getattr(prog, name, None)
            if fn is not None:
                r = _call(fn, op)
                return prog if r is None else r
        return prog

    def _gate(names, *args):
        for name in names:
            fn = getattr(pq, name, None)
            if fn is not None:
                g = _call(fn, *args)
                if g is not None:
                    return g
        return None

    def _controlled_x(control, target):
        g = _gate(("CNOT", "CX", "CNOTGate"), control, target)
        if g is not None:
            return g
        x = _gate(("X", "XGate"), target)
        if x is not None:
            for name in ("control", "set_control"):
                fn = getattr(x, name, None)
                if fn is not None:
                    r = _call(fn, [control])
                    if r is not None:
                        return r
                    r = _call(fn, control)
                    if r is not None:
                        return r
        return None

    def _add_measurements(prog, q, c):
        for name in ("measure_all", "MeasureAll"):
            fn = getattr(pq, name, None)
            if fn is not None:
                m = _call(fn, q, c)
                if m is not None:
                    return _append(prog, m)
                m = _call(fn, q)
                if m is not None:
                    return _append(prog, m)
        for i in range(2):
            m = _gate(("Measure", "measure"), q[i], c[i])
            if m is not None:
                prog = _append(prog, m)
        return prog

    def _build_program(measured):
        qvm = _make_machine()
        q = _alloc_many(qvm, 2, ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "allocateQubits"), ("qAlloc", "qalloc", "allocate_qubit", "allocateQubit"))
        c = _alloc_many(qvm, 2, ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits", "allocateCBits"), ("cAlloc", "calloc", "allocate_cbit", "allocateCBit"))
        prog = _new_prog()
        prog = _append(prog, _gate(("H", "HGate"), q[0]))
        prog = _append(prog, _controlled_x(q[0], q[1]))
        if measured:
            prog = _add_measurements(prog, q, c)
        return qvm, q, c, prog

    qvm, q, c, prog = _build_program(True)

    sample_calls = []
    for owner in (qvm, pq):
        if owner is None:
            continue
        for name in ("run_with_configuration", "runWithConfiguration"):
            fn = getattr(owner, name, None)
            if fn is not None:
                sample_calls.extend([(fn, (prog, c, shots)), (fn, (prog, shots)), (fn, (prog, c))])
        for name in ("run", "sampling", "sample"):
            fn = getattr(owner, name, None)
            if fn is not None:
                sample_calls.extend([(fn, (prog, shots)), (fn, (prog, c, shots)), (fn, (prog, q, shots))])

    for fn, args in sample_calls:
        r = _call(fn, *args)
        p = _normalize(r)
        if p is not None:
            return p

    qvm, q, c, prog = _build_program(False)

    prob_calls = []
    for owner in (qvm, pq):
        if owner is None:
            continue
        for name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list", "prob_run_list", "pmeasure", "pMeasure"):
            fn = getattr(owner, name, None)
            if fn is not None:
                prob_calls.extend([(fn, (prog, q, -1)), (fn, (prog, q)), (fn, (prog, q, 2))])

    for fn, args in prob_calls:
        r = _call(fn, *args)
        p = _normalize(r)
        if p is not None:
            return p

    for owner in (qvm, pq):
        if owner is None:
            continue
        direct = None
        for name in ("directly_run", "directlyRun", "run"):
            direct = getattr(owner, name, None)
            if direct is not None:
                break
        if direct is not None:
            _call(direct, prog)
            for qm_owner in (qvm, pq):
                if qm_owner is None:
                    continue
                qm = getattr(qm_owner, "quick_measure", None)
                if qm is not None:
                    r = _call(qm, q, shots)
                    p = _normalize(r)
                    if p is not None:
                        return p
            for state_name in ("get_qstate", "get_qstate_vector", "get_state", "get_state_vector"):
                getter = getattr(owner, state_name, None)
                if getter is not None:
                    p = _state_to_probs(_call(getter))
                    if p is not None:
                        return p

    raise RuntimeError("Unable to execute Bell-state program with pyQPanda3")
