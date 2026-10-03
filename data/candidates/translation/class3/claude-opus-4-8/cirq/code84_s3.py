# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np


def _u3_matrix(theta, phi, lam):
    return np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)],
    ], dtype=complex)


def controlled_custom_unitary_circuit():
    q = cirq.LineQubit.range(2)
    u3 = cirq.MatrixGate(_u3_matrix(0.3, 0.2, 0.1))
    controlled = u3.controlled()
    circuit = cirq.Circuit()
    circuit.append(controlled.on(q[0], q[1]))
    return circuit
