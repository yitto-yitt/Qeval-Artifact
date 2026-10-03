# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    state = np.asarray(data, dtype=complex)
    if state.ndim != 1:
        state = state.reshape(-1)

    dim = state.size
    num_qubits_float = np.log2(dim)
    num_qubits = int(round(num_qubits_float))
    if 2 ** num_qubits != dim:
        raise ValueError("Input state dimension is not a power of 2.")

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = np.zeros((dim_A, dim_B), dtype=complex)

    for full_index, amplitude in enumerate(state):
        row = 0
        for pos, qubit in enumerate(qargs_A):
            row |= ((full_index >> qubit) & 1) << pos

        col = 0
        for pos, qubit in enumerate(qargs_B):
            col |= ((full_index >> qubit) & 1) << pos

        matrix[row, col] = amplitude

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if not np.isclose(coeff, 0.0):
            terms.append((coeff, u[:, i], vh[i, :]))

    return terms
