# EVAL_META: task_id=120, framework=cirq, class=3
import numpy as np
import cirq

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    if 2 ** n != len(diag):
        raise ValueError("Length of diag must be a power of two")
    qubits = cirq.LineQubit.range(n)
    gate = cirq.MatrixGate(np.diag(diag))
    return cirq.Circuit(gate.on(*qubits))
