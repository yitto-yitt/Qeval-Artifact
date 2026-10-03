# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix


def schmidt_test(data, qargs_B):
    if isinstance(data, Statevector):
        sv = data
    elif isinstance(data, DensityMatrix):
        sv = data.to_statevector()
    else:
        arr = np.asarray(data)
        if arr.ndim == 1:
            sv = Statevector(arr)
        else:
            sv = DensityMatrix(arr).to_statevector()

    dims = sv.dims()
    num_qubits = len(dims)

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A])) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B])) if qargs_B else 1

    vec = np.asarray(sv.data).reshape([d for d in reversed(dims)])

    perm = [num_qubits - 1 - q for q in qargs_A] + [num_qubits - 1 - q for q in qargs_B]
    vec = np.transpose(vec, perm)
    mat = vec.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i in range(len(S)):
        coeff = float(S[i])
        if coeff < 1e-12:
            continue
        state_A = Statevector(U[:, i], dims=[dims[q] for q in qargs_A]) if qargs_A else Statevector(np.array([U[0, i]]))
        state_B = Statevector(Vh[i, :], dims=[dims[q] for q in qargs_B]) if qargs_B else Statevector(np.array([Vh[i, 0]]))
        terms.append((coeff, state_A, state_B))

    return terms
