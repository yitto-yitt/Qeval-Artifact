# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    from_density = False
    if arr.ndim == 0:
        psi = arr.reshape(1)
    elif arr.ndim == 1:
        psi = arr.reshape(-1)
    elif arr.ndim == 2 and 1 in arr.shape:
        psi = arr.reshape(-1)
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        rho = arr
        vals, vecs = np.linalg.eigh((rho + rho.conj().T) / 2)
        idx = int(np.argmax(vals.real))
        max_val = float(vals[idx].real)
        if max_val < -1e-10:
            raise ValueError("Input density matrix is not positive semidefinite.")
        vals_clipped = np.maximum(vals.real, 0.0)
        if np.sum(vals_clipped) > 0 and (np.sum(vals_clipped) - max(max_val, 0.0)) > 1e-8 * max(1.0, np.sum(vals_clipped)):
            raise ValueError("Schmidt decomposition is only defined for pure states.")
        psi = np.sqrt(max(max_val, 0.0)) * vecs[:, idx]
        if psi.size:
            phase_idx = int(np.argmax(np.abs(psi)))
            if abs(psi[phase_idx]) > 0:
                psi = psi / (psi[phase_idx] / abs(psi[phase_idx]))
        from_density = True
    else:
        psi = arr.reshape(-1)

    dim = int(psi.size)
    if dim <= 0 or dim & (dim - 1):
        raise ValueError("Input state dimension is not a power of 2.")

    num_qubits = int(np.log2(dim)) if dim > 1 else 0
    qargs_B = list(qargs_B)
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem arguments are not allowed.")
    if any((not isinstance(q, (int, np.integer))) or q < 0 or q >= num_qubits for q in qargs_B):
        raise ValueError("Subsystem argument out of range.")

    qargs_B = [int(q) for q in qargs_B]
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dim_A = 1 << len(qargs_A)
    dim_B = 1 << len(qargs_B)
    mat = np.zeros((dim_A, dim_B), dtype=complex)

    for idx, amp in enumerate(psi):
        a_idx = 0
        for pos, q in enumerate(qargs_A):
            a_idx |= ((idx >> q) & 1) << pos
        b_idx = 0
        for pos, q in enumerate(qargs_B):
            b_idx |= ((idx >> q) & 1) << pos
        mat[a_idx, b_idx] = amp

    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    atol = 1e-10
    return [(s[i], u[:, i], vh[i, :]) for i in range(len(s)) if s[i] > atol]
