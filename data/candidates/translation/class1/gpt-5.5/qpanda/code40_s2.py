# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *
import math


def init_random_3qubit(desired_vector):
    probs = [abs(complex(x)) ** 2 for x in desired_vector]
    if len(probs) != 8:
        raise ValueError("desired_vector must have length 8")
    total_in = sum(probs)
    if total_in <= 0:
        raise ValueError("desired_vector must be non-zero")
    probs = [p / total_in for p in probs]

    qvm = CPUQVM()
    for _name in ("init_qvm", "init"):
        if hasattr(qvm, _name):
            getattr(qvm, _name)()
            break

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(3)
    else:
        q = qvm.qalloc_many(3)

    prog = QProg()

    def _add_gate(g):
        nonlocal prog
        prog << g

    def _controlled_ry(target_index, angle, controls):
        if abs(angle) < 1e-15:
            return

        flipped = []
        for idx, val in controls:
            if val == 0:
                _add_gate(X(q[idx]))
                flipped.append(idx)

        gate = RY(q[target_index], angle)
        ctrl_qubits = [q[idx] for idx, _ in controls]
        if ctrl_qubits:
            controlled = gate.control(ctrl_qubits)
            if controlled is not None:
                gate = controlled

        _add_gate(gate)

        for idx in reversed(flipped):
            _add_gate(X(q[idx]))

    def _prepare(sub_probs, remaining, controls):
        if not remaining:
            return

        branch_total = sum(sub_probs)
        if branch_total <= 1e-15:
            return

        half = len(sub_probs) // 2
        p0 = sum(sub_probs[:half])
        p1 = sum(sub_probs[half:])

        theta = 2.0 * math.atan2(math.sqrt(max(p1, 0.0)), math.sqrt(max(p0, 0.0)))
        target = remaining[0]
        _controlled_ry(target, theta, controls)

        if p0 > 1e-15:
            _prepare(sub_probs[:half], remaining[1:], controls + [(target, 0)])
        if p1 > 1e-15:
            _prepare(sub_probs[half:], remaining[1:], controls + [(target, 1)])

    _prepare(probs, [2, 1, 0], [])

    out_qubits = [q[2], q[1], q[0]]

    try:
        raw = qvm.prob_run_dict(prog, out_qubits, -1)
    except TypeError:
        raw = qvm.prob_run_dict(prog, out_qubits)
    except AttributeError:
        try:
            raw = prob_run_dict(prog, out_qubits, -1)
        except TypeError:
            raw = prob_run_dict(prog, out_qubits)

    dist = {}
    for key, value in dict(raw).items():
        k = str(key)
        if k.startswith("0b"):
            k = k[2:]
        k = k.replace(" ", "")
        if len(k) < 3:
            k = k.zfill(3)
        elif len(k) > 3:
            k = k[-3:]
        v = float(value)
        if v > 1e-12:
            dist[k] = dist.get(k, 0.0) + v

    total = sum(dist.values())
    if total > 0:
        dist = {k: v / total for k, v in dist.items()}

    for _name in ("finalize", "finalize_qvm"):
        if hasattr(qvm, _name):
            getattr(qvm, _name)()
            break

    return dist
