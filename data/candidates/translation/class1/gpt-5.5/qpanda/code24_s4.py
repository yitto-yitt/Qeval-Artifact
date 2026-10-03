# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *


def dj_algorithm(oracle):
    def _as_list(x):
        if x is None:
            return []
        if isinstance(x, (list, tuple)):
            return list(x)
        try:
            return list(x)
        except Exception:
            return []

    def _qaddr(q, default):
        for name in ("get_phy_addr", "get_physical_addr", "get_phyaddr", "getPhysicalQubitPtr"):
            f = getattr(q, name, None)
            if callable(f):
                try:
                    v = f()
                    if isinstance(v, int):
                        return v
                except Exception:
                    pass
        for name in ("phy_addr", "physical_addr", "addr", "index"):
            try:
                v = getattr(q, name)
                if isinstance(v, int):
                    return v
            except Exception:
                pass
        return default

    def _get_num_qubits(obj):
        for name in ("num_qubits", "qubit_count", "n_qubits", "n"):
            try:
                v = getattr(obj, name)
                if callable(v):
                    v = v()
                if isinstance(v, int):
                    return v
            except Exception:
                pass
        for name in ("get_qubit_num", "get_qubits_num", "qubits_num", "qubit_num"):
            f = getattr(obj, name, None)
            if callable(f):
                try:
                    v = f()
                    if isinstance(v, int):
                        return v
                except Exception:
                    pass
        return None

    def _get_qubits(obj):
        for name in ("qubits", "qbits", "qvec", "qv", "qs", "_qubits"):
            try:
                v = getattr(obj, name)
                if callable(v):
                    v = v()
                qs = _as_list(v)
                if qs:
                    return qs
            except Exception:
                pass
        for name in ("get_used_qubits", "get_used_qbits", "get_qubits", "get_qbits", "used_qubits"):
            f = getattr(obj, name, None)
            if callable(f):
                try:
                    qs = _as_list(f())
                    if qs:
                        return qs
                except Exception:
                    pass
        return []

    def _get_machine(obj):
        for name in ("machine", "qvm", "_machine", "_qvm"):
            try:
                m = getattr(obj, name)
                if m is not None:
                    return m
            except Exception:
                pass
        return None

    def _init_machine(m):
        for name in ("init_qvm", "init", "initQVM"):
            f = getattr(m, name, None)
            if callable(f):
                try:
                    f()
                    return
                except Exception:
                    pass

    def _alloc_qubits(m, count):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "alloc_qubits", "qAllocMany"):
            f = getattr(m, name, None)
            if callable(f):
                try:
                    return _as_list(f(count))
                except Exception:
                    pass
        return []

    def _oracle_body(obj, qs):
        if callable(obj):
            for args in ((qs,), tuple(qs), ()):
                try:
                    r = obj(*args)
                    if r is not None:
                        return r
                except Exception:
                    pass
        for name in ("circuit", "qcircuit", "prog", "program", "oracle"):
            try:
                v = getattr(obj, name)
                if callable(v):
                    v = v()
                if v is not None:
                    return v
            except Exception:
                pass
        return obj

    def _run_for_state(m, prog):
        for name in ("directly_run", "run_qprog", "run", "execute"):
            f = getattr(m, name, None)
            if callable(f):
                try:
                    f(prog)
                    return True
                except Exception:
                    try:
                        f(prog, 1)
                        return True
                    except Exception:
                        pass
        return False

    def _get_state(m):
        for name in ("get_qstate", "get_qstate_vector", "get_state_vector", "get_state", "state"):
            f = getattr(m, name, None)
            try:
                v = f() if callable(f) else f
                if v is not None:
                    return list(v)
            except Exception:
                pass
        return None

    def _state_probs(state, qs, input_len):
        if input_len == 0:
            return {"": 1.0}
        pos = [_qaddr(qs[i], i) for i in range(len(qs))]
        out = {}
        for idx, amp in enumerate(state):
            p = abs(amp) ** 2
            if p <= 1e-15:
                continue
            bits = []
            for i in range(input_len):
                bits.append((idx >> pos[i]) & 1)
            key = "".join(str(bits[i]) for i in range(input_len - 1, -1, -1))
            out[key] = out.get(key, 0.0) + float(p)
        s = sum(out.values())
        if s:
            out = {k: v / s for k, v in out.items() if v > 1e-12}
        return out

    def _key_str(k, length):
        if length == 0:
            return ""
        if isinstance(k, str):
            s = "".join(ch for ch in k if ch in "01")
            if len(s) < length:
                s = s.zfill(length)
            if len(s) > length:
                s = s[-length:]
            return s
        if isinstance(k, int):
            return format(k, "0{}b".format(length))[-length:]
        try:
            s = "".join(str(int(x)) for x in k)
            if len(s) < length:
                s = s.zfill(length)
            if len(s) > length:
                s = s[-length:]
            return s
        except Exception:
            return str(k)

    def _prob_run(m, prog, input_qs, length):
        if length == 0:
            return {"": 1.0}
        targets = list(reversed(input_qs))
        for name in ("prob_run_dict", "probRunDict", "prob_run"):
            f = getattr(m, name, None)
            if callable(f):
                for args in ((prog, targets, -1), (prog, targets), (prog, input_qs, -1), (prog, input_qs)):
                    try:
                        r = f(*args)
                        d = dict(r)
                        out = {}
                        for k, v in d.items():
                            fv = float(v)
                            if fv > 1e-12:
                                out[_key_str(k, length)] = fv
                        s = sum(out.values())
                        if s:
                            return {k: v / s for k, v in out.items()}
                    except Exception:
                        pass
        return None

    n = _get_num_qubits(oracle)
    qubits = _get_qubits(oracle)

    machine = _get_machine(oracle)
    created_machine = False
    if machine is None:
        machine = CPUQVM()
        created_machine = True
    if created_machine:
        _init_machine(machine)

    if n is None:
        n = len(qubits)

    if not qubits:
        qubits = _alloc_qubits(machine, n)
    elif len(qubits) < n:
        extra = _alloc_qubits(machine, n - len(qubits))
        if extra:
            qubits = list(extra) + list(qubits)

    oracle_circuit = _oracle_body(oracle, qubits)

    prog = QProg()
    if n == 0:
        return {"": 1.0}

    prog << X(qubits[n - 1])
    for q in qubits[:n]:
        prog << H(q)
    prog << oracle_circuit
    for q in qubits[:n]:
        prog << H(q)

    input_qubits = qubits[: n - 1]

    if _run_for_state(machine, prog):
        state = _get_state(machine)
        if state is not None:
            return _state_probs(state, qubits[:n], n - 1)

    probs = _prob_run(machine, prog, input_qubits, n - 1)
    if probs is not None:
        return probs

    return {"": 1.0} if n == 1 else {}
