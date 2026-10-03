# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix


def schmidt_test(data, qargs_B):
    if isinstance(data, Statevector):
        sv = data
    elif isinstance(data, DensityMatrix):
        sv = data.to_statevector()
    else:
        sv = Statevector(data)

    num_qubits = sv.num_qubits
    dims = sv.dims()

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A])) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B])) if qargs_B else 1

    vec = np.asarray(sv.data).reshape([dims[q] for q in reversed(range(num_qubits))])

    perm = [num_qubits - 1 - q for q in qargs_A] + [num_qubits - 1 - q for q in qargs_B]
    vec = np.transpose(vec, perm)
    mat = vec.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat)

    terms = []
    for i, coeff in enumerate(S):
        if coeff <= 1e-12:
            continue
        state_A = Statevector(U[:, i], dims=[dims[q] for q in qargs_A]) if qargs_A else Statevector([1])
        state_B = Statevector(Vh[i, :], dims=[dims[q] for q in qargs_B]) if qargs_B else Statevector([1])
        terms.append((float(coeff), state_A, state_B))

    return terms
