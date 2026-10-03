# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 2:
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        idx = np.argmax(eigenvalues)
        state_vec = eigenvectors[:, idx] * np.sqrt(eigenvalues[idx])
    else:
        state_vec = data.flatten()
    n = int(np.log2(state_vec.shape[0]))
    all_qubits = list(range(n))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]
    state_tensor = state_vec.reshape([2] * n)
    new_order = qargs_A + qargs_B
    state_tensor = np.transpose(state_tensor, new_order)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    state_mat = state_tensor.reshape(dim_A, dim_B)
    U, S, Vh = np.linalg.svd(state_mat, full_matrices=False)
    atol = 1e-10
    idxs = np.where(S > atol)[0]
    terms = []
    for i in idxs:
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vh[i, :]
        terms.append((coeff, state_A, state_B))
    return terms