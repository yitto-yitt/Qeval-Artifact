# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector


def schmidt_test(data, qargs_B):
    arr = np.asarray(data.data if hasattr(data, "data") else data, dtype=complex)

    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        rho = 0.5 * (arr + arr.conj().T)
        diag = np.real(np.diag(rho))
        pivot = int(np.argmax(diag))
        if diag[pivot] > 1e-14:
            psi = rho[:, pivot] / np.sqrt(diag[pivot])
        else:
            vals, vecs = np.linalg.eigh(rho)
            psi = vecs[:, int(np.argmax(np.real(vals)))]
            k = int(np.argmax(np.abs(psi)))
            if np.abs(psi[k]) > 0:
                psi = psi / (psi[k] / np.abs(psi[k]))
    else:
        psi = arr.reshape(-1)

    norm = np.linalg.norm(psi)
    if norm != 0:
        psi = psi / norm

    dim = int(psi.size)
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError("Input dimension must be a power of 2.")

    B = [int(q) for q in qargs_B]
    B_set = set(B)
    A = [q for q in range(n) if q not in B_set]

    dim_A = 1 << len(A)
    dim_B = 1 << len(B)
    mat = np.zeros((dim_A, dim_B), dtype=complex)

    for global_index, amp in enumerate(psi):
        a_index = 0
        b_index = 0
        for pos, q in enumerate(A):
            if (global_index >> q) & 1:
                a_index |= 1 << pos
        for pos, q in enumerate(B):
            if (global_index >> q) & 1:
                b_index |= 1 << pos
        mat[a_index, b_index] = amp

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    cutoff = max(1e-12, 1e-10 * (S[0] if S.size else 1.0))
    dims_A = (2,) * len(A) if A else (1,)
    dims_B = (2,) * len(B) if B else (1,)

    for i, coeff in enumerate(S):
        if coeff <= cutoff:
            continue
        vec_A = U[:, i].copy()
        vec_B = Vh[i, :].copy()

        k = int(np.argmax(np.abs(vec_A)))
        if np.abs(vec_A[k]) > 0:
            phase = vec_A[k] / np.abs(vec_A[k])
            vec_A = vec_A / phase
            vec_B = vec_B * phase

        terms.append((float(np.real_if_close(coeff)), Statevector(vec_A, dims=dims_A), Statevector(vec_B, dims=dims_B)))

    return terms
