# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector


def schmidt_test(data, qargs_B):
    if qargs_B is None:
        qargs_B = []
    elif isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    dims = None
    dims_attr = getattr(data, "dims", None)
    if callable(dims_attr):
        try:
            dims = tuple(int(d) for d in dims_attr())
        except TypeError:
            dims = None

    if hasattr(data, "data") and not isinstance(data, np.ndarray):
        arr = np.asarray(data.data, dtype=complex)
    else:
        arr = np.asarray(data, dtype=complex)

    if arr.ndim == 1:
        psi = arr.reshape(-1).astype(complex)
        dim = psi.size
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        rho = arr.astype(complex)
        dim = rho.shape[0]
        diag = np.real_if_close(np.diag(rho)).real
        idx = int(np.argmax(diag))
        if diag[idx] <= 0:
            psi = np.zeros(dim, dtype=complex)
            psi[0] = 1.0
        else:
            psi = rho[:, idx] / np.sqrt(diag[idx])
    else:
        psi = arr.reshape(-1).astype(complex)
        dim = psi.size

    norm = np.linalg.norm(psi)
    if norm != 0:
        psi = psi / norm

    if dims is None or int(np.prod(dims, dtype=int)) != dim:
        n = int(round(np.log2(dim))) if dim > 0 else 0
        if 2**n == dim:
            dims = (2,) * n
        else:
            dims = (dim,)

    nsubs = len(dims)
    qargs_B = sorted(set(qargs_B))
    qargs_A = [q for q in range(nsubs) if q not in qargs_B]

    dims_A = tuple(dims[q] for q in qargs_A)
    dims_B = tuple(dims[q] for q in qargs_B)
    dim_A = int(np.prod(dims_A, dtype=int)) if dims_A else 1
    dim_B = int(np.prod(dims_B, dtype=int)) if dims_B else 1

    matrix = np.zeros((dim_A, dim_B), dtype=complex)

    strides = [1]
    for d in dims[:-1]:
        strides.append(strides[-1] * int(d))

    for full_index, amp in enumerate(psi):
        digits = [0] * nsubs
        rem = full_index
        for i, d in enumerate(dims):
            digits[i] = rem % int(d)
            rem //= int(d)

        a_index = 0
        mult = 1
        for q in qargs_A:
            a_index += digits[q] * mult
            mult *= int(dims[q])

        b_index = 0
        mult = 1
        for q in qargs_B:
            b_index += digits[q] * mult
            mult *= int(dims[q])

        matrix[a_index, b_index] = amp

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    tol = max(matrix.shape) * np.finfo(float).eps * (float(s[0]) if len(s) else 1.0) * 100
    for k, coeff in enumerate(s):
        if coeff > tol:
            state_A = Statevector(u[:, k], dims=dims_A if dims_A else None)
            state_B = Statevector(vh[k, :], dims=dims_B if dims_B else None)
            terms.append((float(coeff), state_A, state_B))

    return terms
