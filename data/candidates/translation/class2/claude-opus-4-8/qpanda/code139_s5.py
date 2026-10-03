# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QStat, Statevector


def schmidt_test(data, qargs_B):
    if hasattr(data, "data"):
        vec = np.asarray(data.data, dtype=complex).reshape(-1)
    else:
        vec = np.asarray(data, dtype=complex).reshape(-1)

    total_dim = vec.shape[0]
    num_qubits = int(round(np.log2(total_dim)))
    if (1 << num_qubits) != total_dim:
        raise ValueError("State vector length must be a power of 2.")

    all_qubits = list(range(num_qubits))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    dimA = 1 << len(qargs_A)
    dimB = 1 << len(qargs_B)

    def bit_of(index, qubit):
        return (index >> qubit) & 1

    mat = np.zeros((dimA, dimB), dtype=complex)
    for idx in range(total_dim):
        a_index = 0
        for pos, q in enumerate(qargs_A):
            a_index |= bit_of(idx, q) << pos
        b_index = 0
        for pos, q in enumerate(qargs_B):
            b_index |= bit_of(idx, q) << pos
        mat[a_index, b_index] = vec[idx]

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for k in range(S.shape[0]):
        coeff = float(S[k])
        if coeff <= 1e-12:
            continue
        state_A = np.ascontiguousarray(U[:, k], dtype=complex)
        state_B = np.ascontiguousarray(np.conjugate(Vh[k, :]), dtype=complex)
        terms.append((coeff, state_A, state_B))

    return terms
