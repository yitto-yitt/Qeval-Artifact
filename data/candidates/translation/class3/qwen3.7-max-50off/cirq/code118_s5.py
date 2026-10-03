# EVAL_META: task_id=118, framework=cirq, class=3
import cirq
import numpy as np

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    sx = np.array([[0.5 + 0.5j, 0.5 - 0.5j],
                   [0.5 - 0.5j, 0.5 + 0.5j]], dtype=complex)
    mat = np.eye(16, dtype=complex)
    mat[14:, 14:] = sx
    c3sx = cirq.MatrixGate(mat)
    circuit = cirq.Circuit(c3sx.on(*qubits))
    return circuit
