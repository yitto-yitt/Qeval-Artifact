# EVAL_META: task_id=68, framework=qpanda, class=1
import math
import pyqpanda3.core as pq

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = math.pi / cycles

    def _new_qvm():
        qvm = pq.CPUQVM()
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(qvm, name):
                try:
                    getattr(qvm, name)()
                except TypeError:
                    pass
                break
        return qvm

    def _alloc_qubits(qvm, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(qvm, name):
                try:
                    return list(getattr(qvm, name)(n))
                except Exception:
                    pass
        return list(range(n))

    def _alloc_cbits(qvm, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
            if hasattr(qvm, name):
                try:
                    return list(getattr(qvm, name)(n))
                except Exception:
                    pass
        return list(range(n))

    def _append(prog, op):
        try:
            return prog << op
        except Exception:
            if hasattr(prog, "insert"):
                prog.insert(op)
                return prog
            if hasattr(prog, "append"):
                prog.append(op)
                return prog
            raise

    def _ry(q, angle):
        last = None
        for args in ((q, angle), (angle, q)):
            try:
                return pq.RY(*args)
            except Exception as exc:
                last = exc
        raise last

    def _x(q):
        return pq.X(q)

    def _measure(q, c):
        last = None
        for name in ("measure", "Measure"):
            if hasattr(pq, name):
                fn = getattr(pq, name)
                for args in ((q, c), (c, q)):
                    try:
                        return fn(*args)
                    except Exception as exc:
                        last = exc
        raise last

    def _is_numeric(v):
        return isinstance(v, (int, float)) or hasattr(v, "__float__")

    def _extract_counts(res):
        if isinstance(res, dict):
            if all(_is_numeric(v) for v in res.values()):
                return res
            for key in ("counts", "result", "data"):
                if key in res:
                    got = _extract_counts(res[key])
                    if got is not None:
                        return got
        for name in ("get_counts", "get_result", "result"):
            if hasattr(res, name):
                attr = getattr(res, name)
                try:
                    val = attr() if callable(attr) else attr
                    got = _extract_counts(val)
                    if got is not None:
                        return got
                except Exception:
                    pass
        return None

    def _clean_counts(counts):
        cleaned = {}
        for k, v in counts.items():
            if isinstance(k, (list, tuple)):
                key = "".join(str(int(x)) for x in k)
            else:
                key = str(k).replace(" ", "")
                if key.startswith("0b"):
                    key = key[2:]
            cleaned[key] = cleaned.get(key, 0.0) + float(v)
        return cleaned

    def _run_counts(prog, ordered_cbits, nshots):
        qvm = _new_qvm()
        methods = []
        for name in ("run_with_configuration", "run_with_config", "run"):
            if hasattr(qvm, name):
                methods.append(getattr(qvm, name))
        attempts = []
        for method in methods:
            attempts.extend((
                (method, (prog, ordered_cbits, nshots)),
                (method, (prog, nshots, ordered_cbits)),
                (method, (prog, nshots)),
                (method, (prog,)),
            ))
        last_exc = None
        for method, args in attempts:
            try:
                res = method(*args)
                counts = _extract_counts(res)
                if counts is not None:
                    return _clean_counts(counts)
            except Exception as exc:
                last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("Unable to execute pyQPanda3 program")

    def _build_program(live):
        measurements = cycles + 1 if live else 1
        qvm = _new_qvm()
        qubits = _alloc_qubits(qvm, 1)
        cbits = _alloc_cbits(qvm, measurements)
        q = qubits[0]
        prog = pq.QProg()
        if live:
            for i in range(cycles):
                prog = _append(prog, _ry(q, e))
                prog = _append(prog, _measure(q, cbits[i]))
            prog = _append(prog, _measure(q, cbits[-1]))
            ordered = [cbits[-1]] + cbits[:-1]
        else:
            for _ in range(cycles):
                prog = _append(prog, _ry(q, e))
            prog = _append(prog, _measure(q, cbits[0]))
            ordered = [cbits[0]]
        return prog, ordered, measurements

    try:
        prog, ordered, measurements = _build_program(bool(bomb_live))
        counts = _run_counts(prog, ordered, shots)
        live_predictions = dud_predictions = detonations = 0.0

        if bomb_live:
            for key, value in counts.items():
                if not key:
                    continue
                if len(key) < measurements:
                    key = key.zfill(measurements)
                if key[0] == "1":
                    detonations += value
                elif "1" in key[1:]:
                    dud_predictions += value
                else:
                    live_predictions += value
        else:
            live_predictions = counts.get("0", 0.0)
            dud_predictions = counts.get("1", 0.0)
            detonations = 0.0

        total = live_predictions + dud_predictions + detonations
        denom = shots if total > 1.5 else 1.0
        return {
            "live_predictions": live_predictions / denom,
            "dud_predictions": dud_predictions / denom,
            "detonations": detonations / denom,
        }
    except Exception:
        def _one_qubit_sample(initial_one, angle):
            qvm = _new_qvm()
            qubits = _alloc_qubits(qvm, 1)
            cbits = _alloc_cbits(qvm, 1)
            q = qubits[0]
            prog = pq.QProg()
            if initial_one:
                prog = _append(prog, _x(q))
            prog = _append(prog, _ry(q, angle))
            prog = _append(prog, _measure(q, cbits[0]))
            counts = _run_counts(prog, [cbits[0]], 1)
            if not counts:
                return 0
            key = max(counts.items(), key=lambda item: item[1])[0]
            return 1 if "1" in key else 0

        live_predictions = dud_predictions = detonations = 0
        if bomb_live:
            for _ in range(shots):
                state = 0
                seen_one = False
                for _ in range(cycles):
                    state = _one_qubit_sample(state == 1, e)
                    if state == 1:
                        seen_one = True
                if state == 1:
                    detonations += 1
                elif seen_one:
                    dud_predictions += 1
                else:
                    live_predictions += 1
        else:
            prog, ordered, _ = _build_program(False)
            counts = _run_counts(prog, ordered, shots)
            live_predictions = int(round(counts.get("0", 0.0)))
            dud_predictions = int(round(counts.get("1", 0.0)))
            detonations = 0

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
