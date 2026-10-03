# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QStat, StateVector


def schmidt_test(data, qargs_B):
    try:
        vec = np.asarray(data.data, dtype=complex).reshape(-1)
    except AttributeError:
        vec = np.asarray(data, dtype=complex).reshape(-1)

    dim = vec.size
    num_qubits = int(round(np.log2(dim)))
    if (1 << num_qubits) != dim:
        raise ValueError("State vector length must be a power of 2.")

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    all_qubits = list(range(num_qubits))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)
    dA = 1 << nA
    dB = 1 << nB

    def bit_of(index, qubit):
        return (index >> qubit) & 1

    M = np.zeros((dA, dB), dtype=complex)
    for idx in range(dim):
        a = 0
        for pos, q in enumerate(qargs_A):
            a |= bit_of(idx, q) << pos
        b = 0
        for pos, q in enumerate(qargs_B):
            b |= bit_of(idx, q) << pos
        M[a, b] = vec[idx]

    U, S, Vh = np.linalg.svd(M, full_matrices=False)

    terms = []
    for k in range(S.size):
        coeff = float(S[k])
        if coeff <= 1e-12:
            continue
        state_A = U[:, k]
        state_B = np.conjugate(Vh[k, :])
        terms.append((coeff, state_A, state_B))

    return terms
