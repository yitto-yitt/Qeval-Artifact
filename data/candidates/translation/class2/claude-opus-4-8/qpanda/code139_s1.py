# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QStateVector


def schmidt_test(data, qargs_B):
    if isinstance(data, QStateVector):
        state = np.asarray(data.data(), dtype=complex).reshape(-1)
    elif hasattr(data, "data") and callable(getattr(data, "data")):
        try:
            state = np.asarray(data.data(), dtype=complex).reshape(-1)
        except Exception:
            state = np.asarray(data, dtype=complex).reshape(-1)
    else:
        state = np.asarray(data, dtype=complex).reshape(-1)

    dim = state.shape[0]
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("State dimension is not a power of 2")

    all_qubits = list(range(num_qubits))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)
    dA = 2 ** nA
    dB = 2 ** nB

    # Qiskit qubit ordering: little-endian. Bit index i corresponds to qubit i.
    # Amplitude index encodes qubits with qubit 0 as least significant bit.
    M = np.zeros((dA, dB), dtype=complex)
    for idx in range(dim):
        bits = [(idx >> q) & 1 for q in range(num_qubits)]
        a_index = 0
        for pos, q in enumerate(qargs_A):
            a_index |= bits[q] << pos
        b_index = 0
        for pos, q in enumerate(qargs_B):
            b_index |= bits[q] << pos
        M[a_index, b_index] = state[idx]

    U, S, Vh = np.linalg.svd(M, full_matrices=False)

    terms = []
    tol = 1e-12
    for k in range(len(S)):
        coeff = float(S[k])
        if coeff <= tol:
            continue
        vecA = U[:, k]
        vecB = Vh[k, :].conj()
        terms.append((coeff, vecA, vecB))

    return terms
