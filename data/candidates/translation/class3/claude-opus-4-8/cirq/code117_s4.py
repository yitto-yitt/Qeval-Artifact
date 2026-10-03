# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    if isinstance(unitary, np.ndarray):
        matrix = unitary
    elif hasattr(unitary, "data"):
        matrix = np.asarray(unitary.data)
    elif hasattr(unitary, "to_matrix"):
        matrix = np.asarray(unitary.to_matrix())
    else:
        matrix = np.asarray(unitary)

    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, matrix, allow_partial_czs=False
    )
    circuit = cirq.Circuit(operations)
    return circuit
