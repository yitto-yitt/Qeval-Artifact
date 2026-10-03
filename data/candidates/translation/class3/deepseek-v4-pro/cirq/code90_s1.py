# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled() -> cirq.Circuit:
    # 2-qubit unitary: X on first qubit, H on second qubit
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    U = np.kron(X, H)
    gate = cirq.MatrixGate(U)
    controlled_gate = cirq.ControlledGate(gate, num_controls=2)

    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit(
        controlled_gate.on(qubits[0], qubits[3], qubits[1], qubits[2])
    )
    return circuit
