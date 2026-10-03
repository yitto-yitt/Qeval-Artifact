# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        rho = arr
        diag = np.real(np.diag(rho))
        k = int(np.argmax(diag))
        if diag[k] > 1e-14:
            vec = rho[:, k] / np.sqrt(rho[k, k])
        else:
            vals, vecs = np.linalg.eigh(rho)
            vec = vecs[:, int(np.argmax(vals))]
    else:
        vec = arr.reshape(-1).astype(complex)

    norm = np.linalg.norm(vec)
    if norm != 0:
        vec = vec / norm

    dim = vec.size
    n_qubits = int(round(np.log2(dim)))
    if 2 ** n_qubits != dim:
        raise ValueError("Input state dimension is not a power of 2.")

    if qargs_B is None:
        qargs_B = list(range(n_qubits // 2, n_qubits))
    else:
        qargs_B = list(qargs_B)

    qargs_A = [i for i in range(n_qubits) if i not in qargs_B]

    tensor = vec.reshape((2,) * n_qubits, order="F")
    tensor = np.transpose(tensor, axes=qargs_A + qargs_B)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape((dim_A, dim_B), order="F")

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if coeff > 1e-10:
            terms.append((float(coeff), np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))

    return terms
