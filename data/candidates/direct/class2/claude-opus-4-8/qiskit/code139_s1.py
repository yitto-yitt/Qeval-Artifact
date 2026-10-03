# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix


def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        sv = data.to_statevector()
    elif isinstance(data, Statevector):
        sv = data
    else:
        arr = np.asarray(data)
        if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
            sv = DensityMatrix(arr).to_statevector()
        else:
            sv = Statevector(arr)

    n = sv.num_qubits
    vec = np.asarray(sv.data).reshape([2] * n)

    qargs_B = list(qargs_B)
    B = [q for q in qargs_B]
    A = [q for q in range(n) if q not in B]

    perm = A + B
    vec_p = np.transpose(vec, perm)
    dimA = 2 ** len(A)
    dimB = 2 ** len(B)
    M = vec_p.reshape(dimA, dimB)

    U, S, Vh = np.linalg.svd(M, full_matrices=False)

    terms = []
    for i, coeff in enumerate(S):
        if coeff < 1e-12:
            continue
        a_state = Statevector(U[:, i])
        b_state = Statevector(Vh[i, :])
        terms.append((float(coeff), a_state, b_state))

    return terms
