# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QStateVector


def schmidt_test(data, qargs_B):
    sv = data
    if hasattr(sv, "data"):
        sv = sv.data
    sv = np.asarray(sv, dtype=complex).reshape(-1)

    dim = sv.size
    num_qubits = int(round(np.log2(dim)))
    if (1 << num_qubits) != dim:
        raise ValueError("State vector length must be a power of 2")

    qargs_B = [int(q) for q in qargs_B]
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

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
        M[a, b] = sv[idx]

    U, S, Vh = np.linalg.svd(M)

    terms = []
    tol = 1e-12
    for k in range(len(S)):
        coeff = S[k]
        if coeff <= tol:
            continue
        vecA = U[:, k]
        vecB = np.conjugate(Vh[k, :])

        stateA = QStateVector(list(np.asarray(vecA, dtype=complex)))
        stateB = QStateVector(list(np.asarray(vecB, dtype=complex)))

        terms.append((float(coeff), stateA, stateB))

    return terms
