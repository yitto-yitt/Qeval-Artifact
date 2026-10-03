# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if not isinstance(data, np.ndarray) and hasattr(data, "data"):
        arr = np.asarray(data.data, dtype=complex)
    else:
        arr = np.asarray(data, dtype=complex)

    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        vals, vecs = np.linalg.eigh(arr)
        state = vecs[:, int(np.argmax(vals.real))]
    else:
        state = arr.reshape(-1)

    dim = state.size
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("Input state dimension must be a power of 2.")

    qargs_B = list(qargs_B)
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem indices in qargs_B.")
    if any(q < 0 or q >= num_qubits for q in qargs_B):
        raise ValueError("Subsystem index out of range.")

    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    tensor = state.reshape((2,) * num_qubits)
    axes_A = [num_qubits - 1 - q for q in reversed(qargs_A)]
    axes_B = [num_qubits - 1 - q for q in reversed(qargs_B)]
    permuted = np.transpose(tensor, axes_A + axes_B)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = permuted.reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if not np.isclose(coeff, 0):
            terms.append((coeff, u[:, i].copy(), vh[i, :].copy()))
    return terms
