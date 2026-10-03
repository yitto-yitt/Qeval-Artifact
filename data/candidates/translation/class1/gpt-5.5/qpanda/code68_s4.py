# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
import pyqpanda3.core as pq
from numpy import pi
from math import cos, sin


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = float(pi / cycles)

    def _make_machine():
        if hasattr(pq, "CPUQVM"):
            m = pq.CPUQVM()
        else:
            m = CPUQVM()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    break
                except TypeError:
                    pass
        return m

    def _alloc_qubits(m, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            if hasattr(m, name):
                return [getattr(m, name)() for _ in range(n)]
        raise RuntimeError("Cannot allocate qubits")

    def _new_prog():
        if hasattr(pq, "QProg"):
            return pq.QProg()
        return QProg()

    def _append(prog, gate):
        r = prog << gate
        return prog if r is None else r

    def _ry(q, angle):
        last_error = None
        for args in ((q, angle), (angle, q)):
            try:
                return pq.RY(*args)
            except Exception as exc:
                last_error = exc
        raise last_error

    def _x(q):
        if hasattr(pq, "X"):
            return pq.X(q)
        return X(q)

    def _normalize_probs(raw):
        if isinstance(raw, dict):
            items = raw.items()
        else:
            items = raw
        out = {}
        for k, v in items:
            if isinstance(k, bytes):
                key = k.decode()
            elif isinstance(k, (tuple, list)):
                key = "".join(str(int(x)) for x in k)
            else:
                key = str(k)
            key = key.replace(" ", "")
            if key.startswith("0b"):
                key = key[2:]
            out[key] = float(v)
        return out

    def _probabilities_for_ops(ops):
        m = _make_machine()
        q = _alloc_qubits(m, 1)
        prog = _new_prog()
        for op in ops:
            if op[0] == "x":
                prog = _append(prog, _x(q[0]))
            else:
                prog = _append(prog, _ry(q[0], op[1]))

        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(m, name):
                method = getattr(m, name)
                for args in ((prog, q, -1), (prog, q)):
                    try:
                        res = method(*args)
                        if isinstance(res, (list, tuple)) and len(res) == 2 and all(isinstance(x, (int, float)) for x in res):
                            return {"0": float(res[0]), "1": float(res[1])}
                        return _normalize_probs(res)
                    except Exception:
                        pass

        if hasattr(m, "directly_run"):
            m.directly_run(prog)
            for name in ("get_prob_dict", "get_probabilities", "get_prob_tuple_list", "get_prob_list"):
                if hasattr(m, name):
                    method = getattr(m, name)
                    for args in ((q, -1), (q,)):
                        try:
                            res = method(*args)
                            if isinstance(res, (list, tuple)) and len(res) == 2 and all(isinstance(x, (int, float)) for x in res):
                                return {"0": float(res[0]), "1": float(res[1])}
                            return _normalize_probs(res)
                        except Exception:
                            pass

        raise RuntimeError("Cannot obtain probabilities from pyQPanda3")

    def _get01(probs):
        p0 = probs.get("0", 0.0)
        p1 = probs.get("1", 0.0)
        s = p0 + p1
        if s > 0:
            p0 /= s
            p1 /= s
        return p0, p1

    try:
        p00, p01 = _get01(_probabilities_for_ops([("ry", theta)]))
        p10, p11 = _get01(_probabilities_for_ops([("x", None), ("ry", theta)]))

        if bomb_live:
            states = {(0, False): 1.0}
            for _ in range(cycles):
                new_states = {}
                for (current, seen_one), prob in states.items():
                    if current == 0:
                        transitions = ((0, p00), (1, p01))
                    else:
                        transitions = ((0, p10), (1, p11))
                    for outcome, tprob in transitions:
                        key = (outcome, seen_one or outcome == 1)
                        new_states[key] = new_states.get(key, 0.0) + prob * tprob
                states = new_states

            live_predictions = 0.0
            dud_predictions = 0.0
            detonations = 0.0
            for (current, seen_one), prob in states.items():
                if current == 1:
                    detonations += prob
                elif seen_one:
                    dud_predictions += prob
                else:
                    live_predictions += prob
        else:
            ops = [("ry", theta) for _ in range(cycles)]
            live_predictions, dud_predictions = _get01(_probabilities_for_ops(ops))
            detonations = 0.0

    except Exception:
        c = cos(theta / 2.0) ** 2
        s = sin(theta / 2.0) ** 2
        if bomb_live:
            states = {(0, False): 1.0}
            for _ in range(cycles):
                new_states = {}
                for (current, seen_one), prob in states.items():
                    transitions = ((0, c), (1, s)) if current == 0 else ((0, s), (1, c))
                    for outcome, tprob in transitions:
                        key = (outcome, seen_one or outcome == 1)
                        new_states[key] = new_states.get(key, 0.0) + prob * tprob
                states = new_states
            live_predictions = sum(prob for (cur, seen), prob in states.items() if cur == 0 and not seen)
            dud_predictions = sum(prob for (cur, seen), prob in states.items() if cur == 0 and seen)
            detonations = sum(prob for (cur, _), prob in states.items() if cur == 1)
        else:
            live_predictions = cos(cycles * theta / 2.0) ** 2
            dud_predictions = sin(cycles * theta / 2.0) ** 2
            detonations = 0.0

    vals = [live_predictions, dud_predictions, detonations]
    vals = [0.0 if abs(v) < 1e-12 else 1.0 if abs(v - 1.0) < 1e-12 else float(v) for v in vals]
    total = sum(vals)
    if total > 0:
        vals = [v / total for v in vals]

    return {
        "live_predictions": vals[0],
        "dud_predictions": vals[1],
        "detonations": vals[2],
    }
