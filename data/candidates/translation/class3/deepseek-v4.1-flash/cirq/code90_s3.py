# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mat = np.kron(X, H)
    custom_gate = cirq.MatrixGate(mat)
    controlled_gate = cirq.ControlledGate(custom_gate, num_controls=2)
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(controlled_gate.on(qubits[0], qubits[3], qubits[1], qubits[2]))
    return circuit
