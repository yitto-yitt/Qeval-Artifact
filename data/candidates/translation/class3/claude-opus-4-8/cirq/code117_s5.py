# EVAL_META: task_id=117, framework=cirq, class=3
import numpy as np
import cirq


def decompose_unitary(unitary):
    if isinstance(unitary, cirq.Circuit):
        u = unitary.unitary()
    elif hasattr(unitary, "data"):
        u = np.asarray(unitary.data)
    elif hasattr(unitary, "to_matrix"):
        u = np.asarray(unitary.to_matrix())
    else:
        u = np.asarray(unitary)

    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cx_operations(
        q0, q1, u, allow_partial_czs=False
    )
    return cirq.Circuit(operations)
