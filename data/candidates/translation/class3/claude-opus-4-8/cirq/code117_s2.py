# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    if isinstance(unitary, cirq.Circuit):
        unitary = unitary.unitary()
    unitary = np.asarray(unitary, dtype=complex)
    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_cz_operations(
        q0, q1, unitary, allow_partial_czs=False
    )
    circuit = cirq.Circuit(operations)
    return circuit
