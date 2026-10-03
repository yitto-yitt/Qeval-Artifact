# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    if hasattr(data, "data"):
        arr = np.asarray(data.data, dtype=complex)
        dims = tuple(data.dims()) if hasattr(data, "dims") else None
    else:
        arr = np.asarray(data, dtype=complex)
        dims = None

    if arr.ndim == 1:
        psi = arr.astype(complex)
        dim_total = psi.size
    else:
        dim_total = arr.shape[0]
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square.")
        diag = np.real_if_close(np.diag(arr))
        ref = int(np.argmax(np.real(diag)))
        amp = np.sqrt(max(float(np.real(diag[ref])), 0.0))
        if amp > 0:
            psi = arr[:, ref] / amp
        else:
            vals, vecs = np.linalg.eigh(arr)
            psi = vecs[:, int(np.argmax(vals))]
        norm = np.linalg.norm(psi)
        if norm != 0:
            psi = psi / norm

    if dims is None:
        n_float = np.log2(dim_total)
        n = int(round(n_float))
        if 2 ** n != dim_total:
            raise ValueError("Input dimension is not a power of two.")
        dims = (2,) * n
    else:
        dims = tuple(int(d) for d in dims)
        if int(np.prod(dims)) != dim_total:
            n_float = np.log2(dim_total)
            n = int(round(n_float))
            dims = (2,) * n
        else:
            n = len(dims)

    if qargs_B is None:
        qargs_B = []
    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    qargs_B = list(dict.fromkeys(qargs_B))
    qargs_A = [q for q in range(n) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A])) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B])) if qargs_B else 1

    strides = [1]
    for d in dims[:-1]:
        strides.append(strides[-1] * d)

    def pack(digits, qargs):
        out = 0
        mult = 1
        for q in qargs:
            out += digits[q] * mult
            mult *= dims[q]
        return out

    mat = np.zeros((dim_A, dim_B), dtype=complex)
    for idx, amp in enumerate(psi):
        rem = idx
        digits = [0] * n
        for q in range(n):
            digits[q] = rem % dims[q]
            rem //= dims[q]
        a_idx = pack(digits, qargs_A)
        b_idx = pack(digits, qargs_B)
        mat[a_idx, b_idx] = amp

    U, s, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    tol = max(mat.shape) * np.finfo(float).eps * (s[0] if s.size else 0.0)
    for k, coeff in enumerate(s):
        if coeff <= tol:
            continue
        vec_A = np.array(U[:, k], dtype=complex)
        vec_B = np.array(Vh[k, :], dtype=complex)

        nz = np.flatnonzero(np.abs(vec_A) > 1e-12)
        if nz.size:
            phase = np.exp(-1j * np.angle(vec_A[nz[0]]))
            vec_A = phase * vec_A
            vec_B = vec_B / phase

        vec_A = np.where(np.abs(vec_A) < 1e-15, 0.0, vec_A)
        vec_B = np.where(np.abs(vec_B) < 1e-15, 0.0, vec_B)
        terms.append((float(np.real_if_close(coeff)), vec_A, vec_B))

    return terms
