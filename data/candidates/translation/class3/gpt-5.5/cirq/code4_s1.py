# EVAL_META: task_id=4, framework=cirq, class=3
import cirq
import numpy as np

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=complex)
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.MatrixGate(matrix).on(q0, q1))
    return circuit
