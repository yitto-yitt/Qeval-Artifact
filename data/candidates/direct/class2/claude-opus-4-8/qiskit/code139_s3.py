# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, Operator


def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        sv = Statevector(data.to_statevector().data)
    elif isinstance(data, Statevector):
        sv = data
    else:
        arr = np.asarray(data, dtype=complex)
        if arr.ndim == 2:
            sv = Statevector(DensityMatrix(arr).to_statevector().data)
        else:
            sv = Statevector(arr)

    num_qubits = sv.num_qubits
    vec = sv.data

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dimA = 2 ** len(qargs_A)
    dimB = 2 ** len(qargs_B)

    M = np.zeros((dimA, dimB), dtype=complex)
    for idx in range(len(vec)):
        bits = [(idx >> q) & 1 for q in range(num_qubits)]
        a = 0
        for i, q in enumerate(qargs_A):
            a |= bits[q] << i
        b = 0
        for i, q in enumerate(qargs_B):
            b |= bits[q] << i
        M[a, b] = vec[idx]

    U, S, Vh = np.linalg.svd(M)

    terms = []
    tol = 1e-12
    for k in range(len(S)):
        coeff = S[k]
        if coeff <= tol:
            continue
        state_A = Statevector(U[:, k])
        state_B = Statevector(np.conj(Vh[k, :]))
        terms.append((coeff, state_A, state_B))

    return terms
