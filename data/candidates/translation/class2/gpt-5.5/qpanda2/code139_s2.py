# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    raw = data
    if not isinstance(data, np.ndarray) and hasattr(data, "data"):
        raw = data.data

    arr = np.asarray(raw, dtype=complex)

    if arr.ndim == 2:
        if arr.shape[0] == 1 or arr.shape[1] == 1:
            state = arr.reshape(-1)
        elif arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            idx = int(np.argmax(vals.real))
            state = vecs[:, idx] * np.sqrt(max(vals[idx].real, 0.0))
            nz = np.flatnonzero(np.abs(state) > 1e-12)
            if nz.size:
                phase = np.angle(state[nz[0]])
                state = state * np.exp(-1j * phase)
        else:
            state = arr.reshape(-1)
    else:
        state = arr.reshape(-1)

    dim = state.size
    n_float = np.log2(dim)
    n = int(round(n_float))
    if 2 ** n != dim:
        raise ValueError("Input state dimension is not a power of 2.")

    if qargs_B is None:
        B = list(range(n // 2))
    elif isinstance(qargs_B, (int, np.integer)):
        B = [int(qargs_B)]
    else:
        B = [int(q) for q in qargs_B]

    if len(set(B)) != len(B) or any(q < 0 or q >= n for q in B):
        raise ValueError("Invalid subsystem qargs.")

    A = [q for q in range(n) if q not in set(B)]

    dim_A = 1 << len(A)
    dim_B = 1 << len(B)
    mat = np.zeros((dim_A, dim_B), dtype=complex)

    for full_index, amp in enumerate(state):
        row = 0
        col = 0
        for k, q in enumerate(A):
            if (full_index >> q) & 1:
                row |= 1 << k
        for k, q in enumerate(B):
            if (full_index >> q) & 1:
                col |= 1 << k
        mat[row, col] = amp

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if not np.isclose(coeff, 0):
            terms.append((coeff, np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))
    return terms
