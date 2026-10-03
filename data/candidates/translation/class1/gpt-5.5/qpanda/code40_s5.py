# EVAL_META: task_id=40, framework=qpanda, class=1
import math
import cmath
import numpy as np
import pyqpanda3.core as pq

def init_random_3qubit(desired_vector):
    eps = 1e-12

    def _call_first(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                fn = getattr(obj, name)
                try:
                    return fn(*args)
                except TypeError:
                    continue
        raise AttributeError(names[0])

    def _init_machine():
        m = pq.CPUQVM()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    break
                except TypeError:
                    try:
                        getattr(m, name)(0)
                        break
                    except Exception:
                        pass
                except Exception:
                    pass
        return m

    def _alloc_many(m, n, is_cbit=False):
        if is_cbit:
            names_many = ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany")
            names_one = ("cAlloc", "calloc")
        else:
            names_many = ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany")
            names_one = ("qAlloc", "qalloc")
        for name in names_many:
            if hasattr(m, name):
                return list(getattr(m, name)(n))
        out = []
        for _ in range(n):
            out.append(_call_first(m, names_one))
        return out

    machine = _init_machine()
    q = _alloc_many(machine, 3, False)
    prog = pq.QProg()

    vec = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vec.size != 8:
        raise ValueError("desired_vector must have length 8")
    norm = np.linalg.norm(vec)
    if norm <= eps:
        raise ValueError("desired_vector must be non-zero")
    vec = vec / norm

    def _append_gate(gate, controls):
        neg = [qb for qb, val in controls if val == 0]
        ctrl_qubits = [qb for qb, _ in controls]
        for qb in neg:
            prog << pq.X(qb)
        if ctrl_qubits:
            gate = gate.control(ctrl_qubits)
        prog << gate
        for qb in reversed(neg):
            prog << pq.X(qb)

    def _phase_gate(qb, angle):
        for name in ("U1", "P", "Phase", "PHASE"):
            if hasattr(pq, name):
                return getattr(pq, name)(qb, angle)
        return pq.U3(qb, 0.0, angle, 0.0)

    def _append_state_qubit(qb, theta, phi, controls):
        if hasattr(pq, "U3"):
            if abs(theta) > eps or abs(phi) > eps:
                _append_gate(pq.U3(qb, theta, phi, 0.0), controls)
        else:
            if abs(theta) > eps:
                _append_gate(pq.RY(qb, theta), controls)
            if abs(phi) > eps:
                _append_gate(_phase_gate(qb, phi), controls)

    def _first_phase(arr):
        for z in arr:
            if abs(z) > eps:
                return cmath.phase(z)
        return 0.0

    def _prepare_state(state, qubits, controls):
        n = len(qubits)
        if n == 0:
            return
        if n == 1:
            a, b = state[0], state[1]
            theta = 2.0 * math.atan2(abs(b), abs(a))
            pa = cmath.phase(a) if abs(a) > eps else 0.0
            pb = cmath.phase(b) if abs(b) > eps else 0.0
            phi = pb - pa
            _append_state_qubit(qubits[0], theta, phi, controls)
            return

        half = 1 << (n - 1)
        s0 = state[:half]
        s1 = state[half:]
        n0 = float(np.linalg.norm(s0))
        n1 = float(np.linalg.norm(s1))
        g0 = _first_phase(s0) if n0 > eps else 0.0
        g1 = _first_phase(s1) if n1 > eps else 0.0

        theta = 2.0 * math.atan2(n1, n0)
        phi = g1 - g0
        parent = qubits[-1]
        _append_state_qubit(parent, theta, phi, controls)

        if n0 > eps:
            _prepare_state(s0 / (n0 * cmath.exp(1j * g0)), qubits[:-1], controls + [(parent, 0)])
        if n1 > eps:
            _prepare_state(s1 / (n1 * cmath.exp(1j * g1)), qubits[:-1], controls + [(parent, 1)])

    _prepare_state(vec, q, [])

    def _format_dist(d):
        out = {}
        for k, v in dict(d).items():
            p = float(np.real(v))
            if p <= 1e-12:
                continue
            if isinstance(k, int):
                s = format(k, "03b")
            else:
                s = str(k).replace(" ", "")
                if s.startswith("0b"):
                    s = s[2:]
                if s.startswith("0x"):
                    s = format(int(s, 16), "03b")
                if len(s) < 3:
                    s = s.zfill(3)
                elif len(s) > 3:
                    s = s[-3:]
            out[s] = out.get(s, 0.0) + p
        total = sum(out.values())
        return {k: v / total for k, v in out.items()} if total else out

    meas_q = [q[2], q[1], q[0]]

    for args in ((prog, meas_q, -1), (prog, meas_q)):
        if hasattr(machine, "prob_run_dict"):
            try:
                return _format_dist(machine.prob_run_dict(*args))
            except Exception:
                pass

    for args in ((prog, meas_q, -1), (prog, meas_q)):
        if hasattr(machine, "prob_run_list"):
            try:
                probs = list(machine.prob_run_list(*args))
                return {format(i, "03b"): float(p) for i, p in enumerate(probs[:8]) if float(p) > 1e-12}
            except Exception:
                pass

    for run_name in ("directly_run", "direct_run", "run"):
        if hasattr(machine, run_name):
            try:
                getattr(machine, run_name)(prog)
                for get_name in ("get_prob_dict", "getProbDict", "probability"):
                    if hasattr(machine, get_name):
                        try:
                            return _format_dist(getattr(machine, get_name)(meas_q, -1))
                        except Exception:
                            try:
                                return _format_dist(getattr(machine, get_name)(meas_q))
                            except Exception:
                                pass
                for get_name in ("get_qstate", "getQState", "get_qstate_vector", "getQStateVector"):
                    if hasattr(machine, get_name):
                        try:
                            state = list(getattr(machine, get_name)())
                            probs = {}
                            for i in range(min(8, len(state))):
                                p = abs(complex(state[i])) ** 2
                                if p > 1e-12:
                                    probs[format(i, "03b")] = p
                            total = sum(probs.values())
                            return {k: v / total for k, v in probs.items()}
                        except Exception:
                            pass
            except Exception:
                pass

    c = _alloc_many(machine, 3, True)
    mprog = pq.QProg()
    mprog << prog
    if hasattr(pq, "measure_all"):
        mprog << pq.measure_all(q, c)
    else:
        for i in range(3):
            mprog << pq.Measure(q[i], c[i])
    counts = machine.run_with_configuration(mprog, c, 4096)
    dist = _format_dist(counts)
    return dist
