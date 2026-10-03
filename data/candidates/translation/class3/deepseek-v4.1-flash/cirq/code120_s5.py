# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n_qubits = len(diag).bit_length() - 1
    qubits = cirq.LineQubit.range(n_qubits)
    matrix = np.diag(diag)
    gate = cirq.MatrixGate(matrix)
    return cirq.Circuit(gate(*qubits))
