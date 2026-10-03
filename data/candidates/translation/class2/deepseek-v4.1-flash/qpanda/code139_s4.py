# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QStat

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        psi = np.asarray(data.data, dtype=complex)
    else:
        psi = np.asarray(data, dtype=complex)

    n = int(np.log2(psi.shape[0]))
    if 2**n != psi.shape[0]:
        raise ValueError("State vector length must be a power of 2")

    qargs_A = [q for q in range(n) if q not in qargs_B]
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)

    psi_new = np.zeros(dim_A * dim_B, dtype=complex)
    for j in range(dim_A * dim_B):
        index_A = j % dim_A
        index_B = j // dim_A
        bits = {}
        for i, qubit in enumerate(qargs_A):
            bits[qubit] = (index_A >> i) & 1
        for i, qubit in enumerate(qargs_B):
            bits[qubit] = (index_B >> i) & 1
        orig_index = 0
        for qubit in range(n):
            if bits[qubit]:
                orig_index |= (1 << qubit)
        psi_new[j] = psi[orig_index]

    mat = psi_new.reshape((dim_A, dim_B), order='F')
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    result = []
    for i in range(len(S)):
        if S[i] > 1e-14:
            coeff = S[i]
            state_A = QStat(U[:, i].tolist())
            state_B = QStat(Vh[i, :].tolist())
            result.append((coeff, state_A, state_B))
    return result
