# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from pyqpanda import *


def schmidt_test(data, qargs_B):
    # Obtain a complex numpy representation of the input state.
    if isinstance(data, np.ndarray):
        arr = np.asarray(data, dtype=complex)
    elif hasattr(data, "data") and not isinstance(data.data, memoryview):
        arr = np.asarray(data.data, dtype=complex)
    else:
        arr = np.asarray(data, dtype=complex)

    # A density matrix (pure state) is converted to its state vector.
    if arr.ndim == 2:
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.abs(vals)))
        arr = vecs[:, idx]

    arr = arr.flatten()
    n = int(round(np.log2(arr.size)))

    # Normalise the B-subsystem qubit indices.
    if qargs_B is None:
        qargs_B = []
    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    elif isinstance(qargs_B, set):
        qargs_B = sorted(qargs_B)
    else:
        qargs_B = list(qargs_B)

    seen = set()
    qb = []
    for q in qargs_B:
        q = int(q) % n
        if q not in seen:
            seen.add(q)
            qb.append(q)

    qa = [i for i in range(n) if i not in seen]

    # Reshape and permute the state vector so that the A subsystem
    # (complement of B) is the row index and B is the column index.
    tensor = arr.reshape((2,) * n)
    tensor = np.transpose(tensor, qa + qb)

    dA = 1 << len(qa)
    dB = 1 << len(qb)
    matrix = tensor.reshape(dA, dB)

    # Singular value decomposition gives the Schmidt coefficients and bases.
    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i in range(len(s)):
        if np.isclose(s[i], 0):
            continue
        terms.append((
            complex(s[i]),
            np.asarray(u[:, i], dtype=complex),
            np.asarray(vh[i, :], dtype=complex),
        ))
    return terms
