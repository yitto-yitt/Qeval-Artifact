# EVAL_META: task_id=4, framework=cirq, class=3
import cirq
import numpy as np

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(2)
    circuit.append(cirq.MatrixGate(np.array(matrix)).on(*qubits))
    return circuit
