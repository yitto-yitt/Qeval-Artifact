# EVAL_META: task_id=84, framework=cirq, class=3
import numpy as np
import cirq


def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    u3 = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2),
         np.exp(1j * (phi + lam)) * np.cos(theta / 2)],
    ])
    q0, q1 = cirq.LineQubit.range(2)
    custom_gate = cirq.MatrixGate(u3).controlled()
    circuit = cirq.Circuit()
    circuit.append(custom_gate.on(q0, q1))
    return circuit
