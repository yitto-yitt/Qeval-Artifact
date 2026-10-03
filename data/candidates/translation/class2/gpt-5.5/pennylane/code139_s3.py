# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 2 and 1 in arr.shape:
        state = arr.reshape(-1)
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(vals.real))
        scale = np.sqrt(max(float(vals[idx].real), 0.0))
        state = scale * vecs[:, idx]
    else:
        state = arr.reshape(-1)

    dim = state.size
    num_qubits = int(round(np.log2(dim))) if dim > 0 else 0
    if 2 ** num_qubits != dim:
        raise ValueError("Input state dimension is not a power of 2.")

    if qargs_B is None:
        qargs_B = []
    elif np.isscalar(qargs_B):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    qargs_B = sorted(qargs_B)
    set_B = set(qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in set_B]

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = np.zeros((dim_A, dim_B), dtype=complex)

    for basis_index, amp in enumerate(state):
        idx_A = 0
        idx_B = 0

        for pos, q in enumerate(qargs_A):
            idx_A |= ((basis_index >> q) & 1) << pos

        for pos, q in enumerate(qargs_B):
            idx_B |= ((basis_index >> q) & 1) << pos

        mat[idx_A, idx_B] = amp

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    return [
        (float(s[i]), np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex))
        for i in range(len(s))
        if not np.isclose(s[i], 0.0)
    ]
