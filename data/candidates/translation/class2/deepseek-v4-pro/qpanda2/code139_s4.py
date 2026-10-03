# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data)

    if arr.ndim == 1:
        vec = arr.astype(complex)
        dim = vec.shape[0]
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square")
        dim = arr.shape[0]
        vals, vecs = np.linalg.eigh(arr)
        vec = vecs[:, int(np.argmax(vals))].astype(complex)
    else:
        raise ValueError("Input must be a state vector or density matrix")

    n = int(np.round(np.log2(dim)))
    if 2 ** n != dim:
        raise ValueError("Dimension must be a power of 2")

    B = sorted(int(q) for q in qargs_B)
    A = [i for i in range(n) if i not in B]

    tensor = np.reshape(vec, [2] * n)
    # Qiskit uses little-endian ordering, so initial tensor axes are
    # (n-1, ..., 0). Move A and B subsystems to the front in that order.
    perm = [n - 1 - i for i in A] + [n - 1 - i for i in B]
    tensor = np.transpose(tensor, perm)

    dim_a = 2 ** len(A)
    dim_b = 2 ** len(B)
    mat = np.reshape(tensor, (dim_a, dim_b))

    U, s, Vh = np.linalg.svd(mat, full_matrices=False)

    def subsystem_vector(raw, num_qubits):
        if num_qubits == 0:
            return raw.copy()
        return np.reshape(raw, [2] * num_qubits).transpose(
            list(reversed(range(num_qubits)))
        ).flatten()

    terms = []
    for k in range(len(s)):
        coeff = s[k]
        if coeff < 1e-10:
            continue
        vec_a = subsystem_vector(U[:, k], len(A))
        vec_b = subsystem_vector(Vh[k].conj(), len(B))
        terms.append((coeff, vec_a, vec_b))

    return terms
