# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n = (len(diag) - 1).bit_length()
    qubits = cirq.LineQubit.range(n)
    matrix = np.diag(diag).astype(np.complex128)
    gate = cirq.MatrixGate(matrix)
    return cirq.Circuit(gate.on(*qubits))
