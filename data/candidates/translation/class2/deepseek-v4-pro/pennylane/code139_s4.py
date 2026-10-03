# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        evals, evecs = np.linalg.eigh(arr)
        if not np.isclose(evals[-1], 1.0):
            raise ValueError("Schmidt decomposition is only defined for pure states")
        state = np.ascontiguousarray(evecs[:, -1])
    elif arr.ndim == 1:
        state = np.ascontiguousarray(arr)
    else:
        raise ValueError("Input must be a 1D state vector or square density matrix")

    n = state.shape[0].bit_length() - 1
    if 2 ** n != state.shape[0]:
        raise ValueError("State dimension must be a power of 2")

    qargs = list(qargs_B)
    if len(qargs) == 0 or len(qargs) >= n:
        raise ValueError("qargs_B must be a proper subset of qubits")

    qargs_b = sorted(qargs)
    if len(set(qargs_b)) != len(qargs_b) or any(q < 0 or q >= n for q in qargs_b):
        raise ValueError("qargs_B contains invalid or duplicate qubit indices")

    qargs_a = [q for q in range(n) if q not in qargs_b]
    order = qargs_a + qargs_b

    tensor = state.reshape([2] * n)
    transposed = np.transpose(tensor, axes=order)

    dim_a = 2 ** len(qargs_a)
    dim_b = 2 ** len(qargs_b)
    mat = transposed.reshape((dim_a, dim_b))

    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    return [(s[i], u[:, i].copy(), vh[i].copy()) for i in range(len(s))]
