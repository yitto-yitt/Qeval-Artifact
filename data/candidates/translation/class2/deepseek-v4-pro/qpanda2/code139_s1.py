# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from pyqpanda import *


def schmidt_test(data, qargs_B):
    """Return Schmidt decomposition terms for a pure quantum state or density matrix."""
    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 1:
        state = arr
        n = int(round(np.log2(state.shape[0])))
        if 2**n != state.shape[0]:
            raise ValueError("Statevector length must be a power of two")
    elif arr.ndim == 2:
        n = int(round(np.log2(arr.shape[0])))
        if arr.shape != (2**n, 2**n):
            raise ValueError("Density matrix must be square with power-of-two dimensions")

        evals, evecs = np.linalg.eigh(arr)
        order = np.argsort(evals)[::-1]
        evals = evals[order]
        evecs = evecs[:, order]

        trace = float(np.sum(evals))
        if trace <= 0:
            raise ValueError("Invalid density matrix")
        evals = evals / trace

        if not np.isclose(evals[0], 1.0, atol=1e-10):
            raise ValueError("Input density matrix is not pure")

        state = evecs[:, 0]
    else:
        raise ValueError("Input must be a statevector or density matrix")

    norm = np.sqrt(np.vdot(state, state))
    state = state / norm

    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    if len(set(qargs_B)) != len(qargs_B) or any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("Invalid subsystem qubit indices")

    qargs_A = [q for q in range(n) if q not in set(qargs_B)]
    dims = [2] * n

    tensor = np.transpose(state.reshape(dims), axes=qargs_B + qargs_A)
    dim_B = 2 ** len(qargs_B)
    dim_A = 2 ** len(qargs_A)
    mat = tensor.reshape((dim_B, dim_A))

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i in range(len(s)):
        coeff = float(s[i])
        vec_A = vh[i, :].copy()
        vec_B = u[:, i].copy()
        terms.append((coeff, vec_A, vec_B))

    return terms
