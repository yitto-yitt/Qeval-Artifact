# EVAL_META: task_id=120, framework=cirq, class=3
import math
import numpy as np
import cirq

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    qubits = cirq.LineQubit.range(num_qubits)
    matrix = np.diag(np.asarray(diag, dtype=complex))
    gate = cirq.MatrixGate(matrix)
    circuit = cirq.Circuit()
    if num_qubits > 0:
        circuit.append(gate.on(*qubits))
    return circuit
