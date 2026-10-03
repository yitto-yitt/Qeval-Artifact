# EVAL_META: task_id=4, framework=cirq, class=3
import cirq

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qubits = cirq.LineQubit.range(2)
    gate = cirq.MatrixGate(matrix)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
