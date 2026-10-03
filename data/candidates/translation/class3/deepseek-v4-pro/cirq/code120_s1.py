# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    gate = cirq.MatrixGate(np.diag(diag))
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
