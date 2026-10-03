# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    # Create the 2-qubit custom gate: X on qubit 0, H on qubit 1
    # Unitary is X ⊗ H
    X = np.array([[0, 1], [1, 0]])
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    U = np.kron(X, H)
    sub_gate = cirq.MatrixGate(U)
    # Add two control qubits
    controlled_gate = cirq.ControlledGate(sub_gate, num_controls=2)
    # Create 4-qubit circuit
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    # Apply controlled gate: controls are qubits 0 and 3, targets are qubits 1 and 2
    circuit.append(controlled_gate.on(qubits[0], qubits[3], qubits[1], qubits[2]))
    return circuit
