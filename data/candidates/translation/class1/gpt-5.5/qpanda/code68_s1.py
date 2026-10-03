# EVAL_META: task_id=68, framework=qpanda, class=1
import math
import pyqpanda3.core as pq


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    angle = math.pi / cycles

    def _init_machine():
        machine = pq.CPUQVM()
        for name in ("init_qvm", "init", "initialize"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    method()
                    break
                except TypeError:
                    try:
                        method("")
                        break
                    except Exception:
                        pass
                except Exception:
                    pass
        return machine

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "alloc_qubits"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    return list(method(n))
                except Exception:
                    pass
        method = getattr(machine, "qAlloc", None) or getattr(machine, "qalloc", None) or getattr(machine, "allocate_qubit")
        return [method() for _ in range(n)]

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany", "alloc_cbits"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    return list(method(n))
                except Exception:
                    pass
        method = getattr(machine, "cAlloc", None) or getattr(machine, "calloc", None) or getattr(machine, "allocate_cbit")
        return [method() for _ in range(n)]

    def _append(prog, op):
        try:
            prog << op
            return prog
        except Exception:
            try:
                prog.insert(op)
                return prog
            except Exception:
                return prog << op

    def _ry(q, theta):
        try:
            return pq.RY(q, theta)
        except TypeError:
            return pq.RY(theta, q)

    def _measure(q, c):
        return pq.Measure(q, c)

    def _run(machine, prog, cbits, nshots):
        attempts = (
            lambda: machine.run_with_configuration(prog, cbits, nshots),
            lambda: machine.run_with_configuration(prog, nshots, cbits),
            lambda: machine.run(prog, cbits, nshots),
            lambda: machine.run(prog, nshots, cbits),
        )
        last_exc = None
        for attempt in attempts:
            try:
                result = attempt()
                if hasattr(result, "items"):
                    return dict(result)
                if hasattr(result, "get_counts"):
                    return dict(result.get_counts())
                return dict(result)
            except Exception as exc:
                last_exc = exc
        raise last_exc

    def _norm_key(key, n):
        if isinstance(key, str):
            s = "".join(ch for ch in key if ch in "01")
        elif isinstance(key, (tuple, list)):
            s = "".join(str(int(x)) for x in key)
        else:
            s = "".join(ch for ch in str(key) if ch in "01")
        if len(s) < n:
            s = s.zfill(n)
        elif len(s) > n:
            s = s[-n:]
        return s

    def _detect_c0_first(machine):
        q = _alloc_qubits(machine, 2)
        c = _alloc_cbits(machine, 2)
        prog = pq.QProg()
        _append(prog, pq.X(q[0]))
        _append(prog, _measure(q[0], c[0]))
        _append(prog, _measure(q[1], c[1]))
        counts = _run(machine, prog, c, 16)
        key = max(counts, key=counts.get)
        s = _norm_key(key, 2)
        if s == "10":
            return True
        if s == "01":
            return False
        return False

    machine = _init_machine()
    c0_first = _detect_c0_first(machine)

    measurements = cycles + 1 if bomb_live else 1
    q = _alloc_qubits(machine, 1)
    c = _alloc_cbits(machine, measurements)
    prog = pq.QProg()

    for i in range(cycles):
        _append(prog, _ry(q[0], angle))
        if bomb_live:
            _append(prog, _measure(q[0], c[i]))
    _append(prog, _measure(q[0], c[measurements - 1]))

    counts = _run(machine, prog, c, shots)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for key, value in counts.items():
            s = _norm_key(key, measurements)
            def bit_at_cindex(idx):
                pos = idx if c0_first else measurements - 1 - idx
                return s[pos]
            if bit_at_cindex(cycles) == "1":
                detonations += value
            elif any(bit_at_cindex(i) == "1" for i in range(cycles)):
                dud_predictions += value
            else:
                live_predictions += value
    else:
        for key, value in counts.items():
            s = _norm_key(key, 1)
            if s[-1] == "0":
                live_predictions += value
            else:
                dud_predictions += value
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
