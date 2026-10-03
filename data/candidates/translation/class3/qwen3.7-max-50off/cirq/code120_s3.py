# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    num_qubits = len(diag).bit_length() - 1
    qubits = cirq.LineQubit.range(num_qubits)
    matrix = np.diag(diag)
    gate = cirq.MatrixGate(matrix)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
