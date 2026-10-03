# EVAL_META: task_id=4, framework=cirq, class=3
import cirq
import numpy as np

class CustomUnitary(cirq.Gate):
    def __init__(self, matrix):
        self.matrix = np.array(matrix, dtype=np.complex128)

    def _num_qubits_(self) -> int:
        return 2

    def _unitary_(self) -> np.ndarray:
        return self.matrix

    def _circuit_diagram_info_(self, args):
        return ('U', 'U')

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    gate = CustomUnitary(matrix)
    circuit.append(gate(q0, q1))
    return circuit
