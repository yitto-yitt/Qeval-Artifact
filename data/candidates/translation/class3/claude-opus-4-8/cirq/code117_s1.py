# EVAL_META: task_id=117, framework=cirq, class=3
import numpy as np
import cirq


def decompose_unitary(unitary):
    if isinstance(unitary, cirq.Circuit):
        unitary = unitary.unitary()
    elif hasattr(unitary, "to_matrix"):
        unitary = unitary.to_matrix()
    elif hasattr(unitary, "data"):
        unitary = np.array(unitary.data)
    else:
        unitary = np.array(unitary)

    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, unitary, allow_partial_czs=False
    )

    circuit = cirq.Circuit(operations)
    return circuit
