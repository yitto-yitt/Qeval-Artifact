# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import *

def init_random_3qubit(desired_vector):
    v = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if v.size != 8:
        raise ValueError("desired_vector must have length 8")
    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("desired_vector must be nonzero")
    v = v / norm

    def complete_unitary(first_col):
        n = first_col.size
        cols = [first_col.astype(complex)]
        for i in range(n):
            e = np.zeros(n, dtype=complex)
            e[i] = 1.0
            w = e.copy()
            for b in cols:
                w = w - b * np.vdot(b, w)
            nw = np.linalg.norm(w)
            if nw > 1e-12:
                cols.append(w / nw)
            if len(cols) == n:
                break
        return np.column_stack(cols)

    U = complete_unitary(v)
    matrices = [U, U.T, U.conjugate(), U.conjugate().T]

    def make_args(mat):
        flat_c = [complex(x) for x in mat.reshape(-1, order="C")]
        flat_f = [complex(x) for x in mat.reshape(-1, order="F")]
        args = [mat, mat.tolist(), flat_c, flat_f]
        try:
            args.append(QStat(flat_c))
        except Exception:
            pass
        try:
            args.append(QStat(flat_f))
        except Exception:
            pass
        return args

    def probs_from_state(state):
        arr = np.asarray([complex(x) for x in state[:8]], dtype=complex)
        probs = [float(abs(x) ** 2) for x in arr]
        total = builtins.sum(probs)
        if total <= 0:
            return None
        return {format(i, "03b"): probs[i] / total for i in range(8) if probs[i] / total > 1e-15}

    def try_program(builder):
        machine = CPUQVM()
        machine.init_qvm()
        try:
            q = machine.qAlloc_many(3)
            prog = QProg()
            prog << builder(q)
            machine.directly_run(prog)
            state = machine.get_qstate()
            return probs_from_state(state)
        finally:
            try:
                machine.finalize()
            except Exception:
                pass

    for name in ("amplitude_encode", "AmplitudeEncode"):
        func = globals().get(name)
        if func is not None:
            for order in (0, 1):
                try:
                    if order == 0:
                        res = try_program(lambda q, f=func: f(q, [complex(x) for x in v]))
                    else:
                        res = try_program(lambda q, f=func: f([complex(x) for x in v], q))
                    if res is not None:
                        return res
                except Exception:
                    pass

    for mat in matrices:
        for arg in make_args(mat):
            try:
                res = try_program(lambda q, a=arg: QOracle(q, a))
                if res is not None:
                    return res
            except Exception:
                pass

    for mat in matrices:
        for arg in make_args(mat):
            try:
                res = try_program(lambda q, a=arg: matrix_decompose(q, a))
                if res is not None:
                    return res
            except Exception:
                pass

    machine = CPUQVM()
    machine.init_qvm()
    try:
        q = machine.qAlloc_many(3)
        c = machine.cAlloc_many(3)
        prog = QProg()
        prog << QOracle(q, U.tolist())
        for i in range(3):
            prog << Measure(q[i], c[i])
        shots = 4096
        try:
            machine.set_random_seed(42)
        except Exception:
            pass
        counts = machine.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        try:
            machine.finalize()
        except Exception:
            pass
