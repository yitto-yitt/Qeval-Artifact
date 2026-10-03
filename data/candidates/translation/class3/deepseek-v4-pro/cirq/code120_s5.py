# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    matrix = np.diag(diag)
    gate = cirq.MatrixGate(matrix)
    qubits = cirq.LineQubit.range(n)
    return cirq.Circuit(gate.on(*qubits))
