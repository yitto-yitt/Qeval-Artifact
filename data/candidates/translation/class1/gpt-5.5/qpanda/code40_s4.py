# EVAL_META: task_id=40, framework=qpanda, class=1
import math
import cmath
import numpy as np
from pyqpanda3.core import *

def init_random_3qubit(desired_vector):
    eps = 1e-12
    vec = np.asarray(desired_vector, dtype=complex).flatten()
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector")
    vec = vec / norm

    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(3)
    elif hasattr(qvm, "allocate_qubits"):
        qubits = qvm.allocate_qubits(3)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(3)
    else:
        qubits = [qvm.qAlloc() for _ in range(3)]

    prog = QProg()

    def _append_gate(gate, controls):
        zero_controls = [q for q, v in controls if v == 0]
        all_controls = [q for q, _ in controls]
        for q in zero_controls:
            prog << X(q)
        if all_controls:
            prog << gate.control(all_controls)
        else:
            prog << gate
        for q in reversed(zero_controls):
            prog << X(q)

    def _canonical(v):
        v = np.asarray(v, dtype=complex)
        nrm = np.linalg.norm(v)
        if nrm < eps:
            return 0.0, 0.0, v
        u = v / nrm
        phase = 0.0
        for z in u:
            if abs(z) > eps:
                phase = cmath.phase(z)
                break
        u = u * cmath.exp(-1j * phase)
        return nrm, phase, u

    def _prepare_one(q, a, b, controls):
        ra = abs(a)
        rb = abs(b)
        if ra < eps and rb < eps:
            return
        theta = 2.0 * math.atan2(rb, ra)
        phi = 0.0
        if rb >= eps:
            phi = cmath.phase(b) - (cmath.phase(a) if ra >= eps else 0.0)
        if abs(phi) > eps:
            _append_gate(RZ(q, -phi), controls)
        if abs(theta) > eps:
            _append_gate(RY(q, theta), controls)
        if abs(phi) > eps:
            _append_gate(RZ(q, phi), controls)

    def _prepare_state(v, qs, controls):
        m = len(qs)
        if m == 1:
            _prepare_one(qs[0], v[0], v[1], controls)
            return

        half = 1 << (m - 1)
        v0 = v[:half]
        v1 = v[half:]

        p0 = float(np.vdot(v0, v0).real)
        p1 = float(np.vdot(v1, v1).real)

        n0, g0, u0 = _canonical(v0)
        n1, g1, u1 = _canonical(v1)

        rel = 0.0
        if p0 > eps and p1 > eps:
            rel = g1 - g0

        _prepare_one(qs[0], math.sqrt(max(p0, 0.0)), math.sqrt(max(p1, 0.0)) * cmath.exp(1j * rel), controls)

        if p0 > eps:
            _prepare_state(u0, qs[1:], controls + [(qs[0], 0)])
        if p1 > eps:
            _prepare_state(u1, qs[1:], controls + [(qs[0], 1)])

    logical_qubits = [qubits[2], qubits[1], qubits[0]]
    _, _, canonical_vec = _canonical(vec)
    _prepare_state(canonical_vec, logical_qubits, [])

    if hasattr(qvm, "prob_run_dict"):
        try:
            probs = qvm.prob_run_dict(prog, logical_qubits, -1)
        except TypeError:
            probs = qvm.prob_run_dict(prog, logical_qubits)
    elif hasattr(qvm, "prob_run_tuple_list"):
        probs = dict(qvm.prob_run_tuple_list(prog, logical_qubits, -1))
    else:
        if hasattr(qvm, "directly_run"):
            qvm.directly_run(prog)
        elif hasattr(qvm, "run"):
            qvm.run(prog)
        state = qvm.get_qstate()
        probs = {}
        for i, amp in enumerate(state[:8]):
            p = float(abs(amp) ** 2)
            if p > eps:
                probs[format(i, "03b")] = p

    result = {}
    for k, v in dict(probs).items():
        if isinstance(k, int):
            key = format(k, "03b")
        else:
            key = str(k)
        key = key.replace(" ", "")
        if len(key) < 3:
            key = key.zfill(3)
        if len(key) > 3:
            key = key[-3:]
        p = float(v)
        if p > 1e-10:
            result[key] = p

    total = sum(result.values())
    if total > 0:
        result = {k: v / total for k, v in result.items()}
    return result
