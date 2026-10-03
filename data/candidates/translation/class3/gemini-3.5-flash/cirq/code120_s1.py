# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    qubits = cirq.LineQubit.range(n)
    angles = [np.angle(x) for x in diag]
    gate = cirq.DiagonalGate(angles)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
