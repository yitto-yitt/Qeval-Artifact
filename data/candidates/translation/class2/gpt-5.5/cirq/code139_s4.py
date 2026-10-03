# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    def _as_state_vector(obj):
        arr = np.asarray(obj, dtype=complex)
        if arr.ndim == 0 and hasattr(obj, "data"):
            arr = np.asarray(obj.data, dtype=complex)
        if arr.ndim == 1:
            return arr.astype(complex, copy=False)
        if arr.ndim == 2:
            if 1 in arr.shape:
                return arr.reshape(-1).astype(complex, copy=False)
            if arr.shape[0] == arr.shape[1]:
                vals, vecs = np.linalg.eigh(arr)
                idx = int(np.argmax(np.real(vals)))
                val = np.real(vals[idx])
                if val < 0 and abs(val) < 1e-12:
                    val = 0.0
                return (np.sqrt(val) * vecs[:, idx]).astype(complex, copy=False)
        return arr.reshape(-1).astype(complex, copy=False)

    state = _as_state_vector(data)
    dim = int(state.size)
    if dim < 1:
        raise ValueError("Input state vector cannot be empty.")
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("Input state dimension is not a power of 2.")

    if qargs_B is None:
        b_qubits = []
    elif np.isscalar(qargs_B):
        b_qubits = [int(qargs_B)]
    else:
        b_qubits = [int(q) for q in qargs_B]

    if len(set(b_qubits)) != len(b_qubits):
        raise ValueError("Duplicate qargs are not allowed.")
    if any(q < 0 or q >= num_qubits for q in b_qubits):
        raise ValueError("qargs are out of range.")

    b_set = set(b_qubits)
    a_qubits = [q for q in range(num_qubits) if q not in b_set]
    b_qubits_sorted = sorted(b_qubits)

    if len(b_qubits_sorted) == 0:
        return [(1.0, np.array(state, dtype=complex, copy=True), np.array([1.0 + 0.0j]))]
    if len(a_qubits) == 0:
        return [(1.0, np.array([1.0 + 0.0j]), np.array(state, dtype=complex, copy=True))]

    tensor = state.reshape((2,) * num_qubits)
    a_axes = [num_qubits - 1 - q for q in sorted(a_qubits, reverse=True)]
    b_axes = [num_qubits - 1 - q for q in sorted(b_qubits_sorted, reverse=True)]
    matrix = np.transpose(tensor, a_axes + b_axes).reshape(
        2 ** len(a_qubits), 2 ** len(b_qubits_sorted)
    )

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    tol = max(matrix.shape) * (s[0] if s.size else 0.0) * np.finfo(float).eps
    tol = max(tol, 1e-12)

    return [
        (float(s[i]), np.array(u[:, i], dtype=complex, copy=True), np.array(vh[i, :], dtype=complex, copy=True))
        for i in range(len(s))
        if s[i] > tol
    ]
