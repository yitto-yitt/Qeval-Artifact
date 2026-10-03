# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    num_qubits = int(np.log2(len(diag)))
    matrix = np.diag(np.asarray(diag, dtype=complex))
    diagonal_gate = cirq.MatrixGate(matrix)
    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(diagonal_gate.on(*qubits))
