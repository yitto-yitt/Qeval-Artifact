# EVAL_META: task_id=4, framework=cirq, class=3
import cirq
import numpy as np

class CustomUnitary(cirq.Gate):
    def __init__(self, matrix):
        self._matrix = np.array(matrix, dtype=np.complex128)
        
    def _num_qubits_(self):
        return 2
        
    def _unitary_(self):
        return self._matrix
        
    def _circuit_diagram_info_(self, args):
        return ("[U]", "[U]")

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(CustomUnitary(matrix).on(*qubits))
    return circuit
