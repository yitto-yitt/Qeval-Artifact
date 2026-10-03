# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    state = np.asarray(getattr(data, "data", data))

    if state.ndim == 2:
        vals, vecs = np.linalg.eigh(state)
        idx = np.argmax(vals)
        if not np.isclose(np.sum(vals), 1.0) or np.sum(vals > 1e-12) > 1:
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = vecs[:, idx]
        phase = np.exp(-1j * np.angle(state[np.argmax(np.abs(state))]))
        state = state * phase
    else:
        state = state.ravel()

    dim = state.size
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("State dimension must be a power of 2.")

    qargs_B = list(qargs_B)
    all_qubits = list(range(num_qubits))
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)
    dA = 2 ** nA
    dB = 2 ** nB

    # Qiskit qubit i corresponds to tensor axis (num_qubits - 1 - i)
    tensor = state.reshape([2] * num_qubits)

    axes_A = [num_qubits - 1 - q for q in qargs_A]
    axes_B = [num_qubits - 1 - q for q in qargs_B]

    perm = axes_A + axes_B
    mat = np.transpose(tensor, perm).reshape(dA, dB)

    U, S, Vh = np.linalg.svd(mat)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff < 1e-12:
            continue
        vecA = U[:, i]
        vecB = Vh[i, :]
        terms.append((float(coeff), vecA, vecB))

    return terms
