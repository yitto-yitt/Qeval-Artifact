# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    unitary = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    q0, q1 = cirq.LineQubit.range(2)
    circ = cirq.Circuit(cirq.MatrixGate(unitary).on(q0, q1))
    decomposed = cirq.decompose(circ)
    optimized = cirq.merge_single_qubit_gates_to_phased_x_z(cirq.Circuit(decomposed))
    return optimized
