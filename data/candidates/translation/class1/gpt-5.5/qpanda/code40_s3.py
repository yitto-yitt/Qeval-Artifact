# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *
import math
import numpy as np

def init_random_3qubit(desired_vector):
    def _init_machine():
        if "CPUQVM" in globals():
            m = CPUQVM()
        else:
            m = init_quantum_machine(QMachineType.CPU)
        for nm in ("init_qvm", "init"):
            if hasattr(m, nm):
                try:
                    getattr(m, nm)()
                    break
                except TypeError:
                    pass
        return m

    def _alloc_many(machine, n, is_cbit=False):
        names = ("cAlloc_many", "calloc_many", "c_alloc_many") if is_cbit else ("qAlloc_many", "qalloc_many", "q_alloc_many")
        one_names = ("cAlloc", "calloc", "c_alloc") if is_cbit else ("qAlloc", "qalloc", "q_alloc")
        for nm in names:
            if hasattr(machine, nm):
                obj = getattr(machine, nm)(n)
                return [obj[i] for i in range(n)]
        for nm in one_names:
            if hasattr(machine, nm):
                return [getattr(machine, nm)() for _ in range(n)]
        for nm in names:
            if nm in globals():
                obj = globals()[nm](n)
                return [obj[i] for i in range(n)]
        for nm in one_names:
            if nm in globals():
                return [globals()[nm]() for _ in range(n)]
        raise RuntimeError("No allocator available")

    def _ctrl_gate(gate, ctrls):
        if not ctrls:
            return gate
        if hasattr(gate, "control"):
            r = gate.control(ctrls)
            return gate if r is None else r
        if hasattr(gate, "set_control"):
            r = gate.set_control(ctrls)
            return gate if r is None else r
        raise RuntimeError("Controlled gates are not available")

    def _append_controlled_rotation(prog, gate_func, target, angle, controls):
        if abs(angle) < 1e-15:
            return
        ctrl_qubits = [qb for qb, _ in controls]
        gate = _ctrl_gate(gate_func(target, float(angle)), ctrl_qubits)
        flipped = [qb for qb, val in controls if val == 0]
        for qb in flipped:
            prog << X(qb)
        prog << gate
        for qb in reversed(flipped):
            prog << X(qb)

    def _append_basis_phase(prog, q, index, angle):
        if abs(angle) < 1e-15:
            return
        phase_gate_func = globals().get("U1", None) or globals().get("P", None) or globals().get("Phase", None)
        if phase_gate_func is None:
            return
        try:
            gate = _ctrl_gate(phase_gate_func(q[0], float(angle)), [q[1], q[2]])
        except Exception:
            return
        flipped = [q[bit] for bit in range(3) if ((index >> bit) & 1) == 0]
        for qb in flipped:
            prog << X(qb)
        prog << gate
        for qb in reversed(flipped):
            prog << X(qb)

    def _result_to_probs(res):
        out = {}
        if hasattr(res, "items"):
            iterable = res.items()
        else:
            iterable = dict(res).items()
        for k, v in iterable:
            if isinstance(k, int):
                key = format(k, "03b")
            else:
                key = str(k).replace(" ", "")
                if key.startswith("0b"):
                    key = key[2:]
                if len(key) < 3 and all(ch in "01" for ch in key):
                    key = key.zfill(3)
            try:
                val = float(v)
            except Exception:
                val = float(np.real(v))
            if val > 1e-15:
                out[key] = out.get(key, 0.0) + val
        total = sum(out.values())
        if total == 0:
            return out
        return {k: out[k] / total for k in sorted(out)}

    vec = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vec.size != 8:
        raise ValueError("desired_vector must have length 8")
    norm = float(np.linalg.norm(vec))
    if norm == 0.0:
        raise ValueError("desired_vector must be nonzero")
    vec = vec / norm
    mags = np.abs(vec)

    qvm = _init_machine()
    q = _alloc_many(qvm, 3, False)
    prog = QProg()

    n0 = math.sqrt(sum(float(mags[i] * mags[i]) for i in range(4)))
    n1 = math.sqrt(sum(float(mags[i] * mags[i]) for i in range(4, 8)))
    _append_controlled_rotation(prog, RY, q[2], 2.0 * math.atan2(n1, n0), [])

    for b2 in (0, 1):
        inds0 = [i for i in range(8) if ((i >> 2) & 1) == b2 and ((i >> 1) & 1) == 0]
        inds1 = [i for i in range(8) if ((i >> 2) & 1) == b2 and ((i >> 1) & 1) == 1]
        n0 = math.sqrt(sum(float(mags[i] * mags[i]) for i in inds0))
        n1 = math.sqrt(sum(float(mags[i] * mags[i]) for i in inds1))
        _append_controlled_rotation(prog, RY, q[1], 2.0 * math.atan2(n1, n0), [(q[2], b2)])

    for b2 in (0, 1):
        for b1 in (0, 1):
            i0 = (b2 << 2) | (b1 << 1)
            i1 = i0 | 1
            _append_controlled_rotation(prog, RY, q[0], 2.0 * math.atan2(float(mags[i1]), float(mags[i0])), [(q[2], b2), (q[1], b1)])

    phases = np.angle(vec)
    for idx in range(8):
        _append_basis_phase(prog, q, idx, float(phases[idx]))

    q_eval = [q[2], q[1], q[0]]

    for nm in ("prob_run_dict", "probRunDict", "prob_run"):
        if hasattr(qvm, nm):
            method = getattr(qvm, nm)
            for args in ((prog, q_eval, -1), (prog, q_eval)):
                try:
                    return _result_to_probs(method(*args))
                except TypeError:
                    pass

    for nm in ("prob_run_dict", "probRunDict", "prob_run"):
        if nm in globals():
            method = globals()[nm]
            for args in ((prog, q_eval, -1), (prog, q_eval)):
                try:
                    return _result_to_probs(method(*args))
                except TypeError:
                    pass

    c = _alloc_many(qvm, 3, True)
    for i in range(3):
        prog << Measure(q_eval[i], c[i])

    for nm in ("run_with_configuration", "runWithConfiguration"):
        if hasattr(qvm, nm):
            return _result_to_probs(getattr(qvm, nm)(prog, c, 4096))

    raise RuntimeError("No executable probability or sampling method available")
