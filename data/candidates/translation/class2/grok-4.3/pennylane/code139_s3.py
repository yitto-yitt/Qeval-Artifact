# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data).ravel()
    n_qubits = int(np.log2(len(data)))
    qargs_A = sorted(set(range(n_qubits)) - set(qargs_B))
    tensor = data.reshape([2] * n_qubits)
    new_order = qargs_A + qargs_B
    tensor = np.transpose(tensor, new_order)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape((dim_A, dim_B))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i in range(len(S)):
        coeff = S[i]
        vec_A = U[:, i]
        vec_B = np.conj(Vh[i, :])
        terms.append((coeff, vec_A, vec_B))
    return terms
