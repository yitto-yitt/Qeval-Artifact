# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    num_qubits = int(np.round(np.log2(len(diag))))
    qubits = cirq.LineQubit.range(num_qubits)
    angles = np.angle(diag)
    gate = cirq.DiagonalGate(angles)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
