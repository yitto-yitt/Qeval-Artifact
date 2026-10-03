# EVAL_META: task_id=4, framework=cirq, class=3
import numpy as np
import cirq

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=complex)
    qubits = cirq.LineQubit.range(2)
    gate = cirq.MatrixGate(matrix)
    circuit = cirq.Circuit()
    circuit.append(gate(qubits[0], qubits[1]))
    return circuit
