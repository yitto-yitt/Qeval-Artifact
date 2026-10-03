# EVAL_META: task_id=120, framework=cirq, class=3
import math
import numpy as np
import cirq

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    qubits = cirq.LineQubit.range(num_qubits)
    diagonal_gate = cirq.MatrixGate(np.diag(np.asarray(diag, dtype=complex)))
    circuit = cirq.Circuit()
    circuit.append(diagonal_gate.on(*qubits))
    return circuit
