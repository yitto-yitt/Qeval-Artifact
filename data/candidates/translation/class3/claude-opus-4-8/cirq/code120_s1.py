# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    qubits = cirq.LineQubit.range(n)
    gate = cirq.MatrixGate(np.diag(diag))
    circuit = cirq.Circuit()
    circuit.append(gate.on(*qubits))
    return circuit
