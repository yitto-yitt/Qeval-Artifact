# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace, Operator


def schmidt_test(data, qargs_B):
    if isinstance(data, Statevector):
        sv = data
    elif isinstance(data, DensityMatrix):
        sv = data.to_statevector()
    else:
        arr = np.asarray(data, dtype=complex)
        if arr.ndim == 1:
            sv = Statevector(arr)
        elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
            sv = DensityMatrix(arr).to_statevector()
        else:
            sv = Statevector(arr.ravel())

    num_qubits = sv.num_qubits
    dims = sv.dims()

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A])) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B])) if qargs_B else 1

    all_qargs = qargs_A + qargs_B
    perm = np.argsort([num_qubits - 1 - q for q in reversed(all_qargs)])

    vec = np.asarray(sv.data, dtype=complex).reshape([2] * num_qubits)

    axis_order = [num_qubits - 1 - q for q in qargs_A] + \
                 [num_qubits - 1 - q for q in qargs_B]
    vec = np.transpose(vec, axes=axis_order)
    mat = vec.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff < 1e-12:
            continue
        state_A = Statevector(U[:, i], dims=[dims[q] for q in qargs_A]) if qargs_A else U[:, i]
        state_B = Statevector(Vh[i, :], dims=[dims[q] for q in qargs_B]) if qargs_B else Vh[i, :]
        terms.append((coeff, state_A, state_B))

    return terms
