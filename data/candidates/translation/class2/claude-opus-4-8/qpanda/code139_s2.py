# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QStat, StateVector


def schmidt_test(data, qargs_B):
    def _to_statevector(d):
        if isinstance(d, StateVector):
            return np.asarray(d.data(), dtype=complex).reshape(-1)
        if isinstance(d, QStat):
            return np.asarray(list(d), dtype=complex).reshape(-1)
        arr = np.asarray(d, dtype=complex)
        if arr.ndim == 2 and arr.shape[0] == arr.shape[1] and arr.shape[0] > 1:
            w, v = np.linalg.eigh(arr)
            idx = int(np.argmax(w.real))
            vec = v[:, idx]
            phase = np.exp(-1j * np.angle(vec[np.argmax(np.abs(vec) > 1e-12)]))
            return (vec * phase).reshape(-1)
        return arr.reshape(-1)

    vec = _to_statevector(data)
    dim = vec.shape[0]
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("Statevector dimension is not a power of 2.")

    qargs_B = sorted(int(q) for q in qargs_B)
    all_qubits = list(range(num_qubits))
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)
    dA = 2 ** nA
    dB = 2 ** nB

    tensor = vec.reshape([2] * num_qubits)

    axes_order = qargs_A[::-1] + qargs_B[::-1]
    axes_index = [num_qubits - 1 - ax for ax in axes_order]
    permuted = np.transpose(tensor, axes=axes_index)

    matrix = permuted.reshape(dA, dB)

    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        state_A = U[:, i].reshape(-1)
        state_B = Vh[i, :].reshape(-1)
        terms.append((float(coeff), state_A, state_B))

    return terms
