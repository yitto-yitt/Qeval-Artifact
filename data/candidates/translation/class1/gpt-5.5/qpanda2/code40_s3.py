# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import *

def init_random_3qubit(desired_vector):
    dim = 8
    vec = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vec.size != dim:
        raise ValueError("desired_vector must have length 8")
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    vec = vec / norm

    cols = []
    for candidate in [vec] + [np.eye(dim, dtype=complex)[:, i] for i in range(dim)]:
        w = np.array(candidate, dtype=complex, copy=True)
        for col in cols:
            w = w - np.vdot(col, w) * col
        w_norm = np.linalg.norm(w)
        if w_norm > 1e-12:
            cols.append(w / w_norm)
        if len(cols) == dim:
            break
    unitary = np.column_stack(cols)

    flat_unitary = [complex(x) for x in unitary.reshape(-1)]
    nested_unitary = [[complex(unitary[i, j]) for j in range(dim)] for i in range(dim)]

    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(3)
        prog = QProg()

        inserted = False
        last_error = None
        for args in ((qubits, flat_unitary), (qubits, nested_unitary), (qubits, unitary), (flat_unitary, qubits), (nested_unitary, qubits)):
            try:
                circ = matrix_decompose(*args)
                prog.insert(circ)
                inserted = True
                break
            except Exception as exc:
                last_error = exc

        if not inserted:
            oracle = globals().get("QOracle")
            if oracle is not None:
                for mat in (flat_unitary, nested_unitary, unitary):
                    try:
                        prog.insert(oracle(qubits, mat))
                        inserted = True
                        break
                    except Exception as exc:
                        last_error = exc

        if not inserted:
            raise last_error

        try:
            probs = qvm.prob_run_list(prog, qubits, -1)
        except TypeError:
            probs = qvm.prob_run_list(prog, qubits)

        dist = {}
        for i, p in enumerate(probs[:dim]):
            val = float(np.real(p))
            if val > 1e-12:
                dist[format(i, "03b")] = val

        total = builtins.sum(dist.values())
        if total > 0:
            dist = {k: v / total for k, v in dist.items()}
        return dist
    finally:
        try:
            qvm.finalize()
        except Exception:
            pass
