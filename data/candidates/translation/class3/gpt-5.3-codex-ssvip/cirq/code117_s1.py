# EVAL_META: task_id=117, framework=cirq, class=3
import numpy as np
import cirq


def decompose_unitary(unitary):
    u = np.array(unitary, dtype=complex)
    if u.shape != (4, 4):
        raise ValueError("Input unitary must be a 4x4 matrix.")
    q0, q1 = cirq.LineQubit.range(2)
    op = cirq.MatrixGate(u).on(q0, q1)
    circuit = cirq.Circuit(cirq.two_qubit_matrix_to_operations(q0, q1, u, allow_partial_czs=False))
    if len(circuit) == 0:
        circuit = cirq.Circuit(op)
    return circuit
