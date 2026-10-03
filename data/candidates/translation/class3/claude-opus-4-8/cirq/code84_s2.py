# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np


def _u3_matrix(theta, phi, lam):
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([
        [c, -np.exp(1j * lam) * s],
        [np.exp(1j * phi) * s, np.exp(1j * (phi + lam)) * c],
    ], dtype=complex)


def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    qubits = cirq.LineQubit.range(2)
    u3_gate = cirq.MatrixGate(_u3_matrix(theta, phi, lam))
    controlled_gate = u3_gate.controlled()
    circuit = cirq.Circuit()
    circuit.append(controlled_gate.on(qubits[0], qubits[1]))
    return circuit
