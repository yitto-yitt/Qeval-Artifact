# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 2:
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        psi = eigenvectors[:, np.argmax(eigenvalues.real)]
    else:
        psi = data.flatten()
    n = int(np.log2(psi.shape[0]))
    qa = [q for q in range(n) if q not in qargs_B]
    qb = list(qargs_B)
    all_qubits = qa + qb
    psi_tensor = psi.reshape([2] * n)
    psi_tensor = np.transpose(psi_tensor, all_qubits)
    dim_a = 2 ** len(qa)
    dim_b = 2 ** len(qb)
    mat = psi_tensor.reshape((dim_a, dim_b))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    result = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            coeff = S[i]
            vec_a = U[:, i]
            vec_b = Vh[i, :].conj()
            result.append((coeff, vec_a, vec_b))
    return result
