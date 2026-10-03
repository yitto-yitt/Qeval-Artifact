# EVAL_META: task_id=4, framework=pennylane, class=3
import pennylane as qml

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = qml.QuantumScript([qml.QubitUnitary(matrix, wires=[0, 1])])
    return circuit
