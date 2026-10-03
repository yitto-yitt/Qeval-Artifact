# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    num_qubits = int(np.log2(len(diag)))
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    gate = cirq.MatrixGate(np.diag(diag), num_qubits=num_qubits)
    circuit.append(gate.on(*qubits))
    return circuit
