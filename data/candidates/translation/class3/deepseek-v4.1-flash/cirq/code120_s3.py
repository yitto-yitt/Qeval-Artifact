# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    if (1 << n) != len(diag):
        raise ValueError("Length of diag must be a power of 2")
    qubits = cirq.LineQubit.range(n)
    if n == 0:
        return cirq.Circuit()
    gate = cirq.MatrixGate(np.diag(diag))
    return cirq.Circuit(gate.on(*qubits))
