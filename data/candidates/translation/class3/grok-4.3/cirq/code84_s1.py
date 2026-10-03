# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    q0, q1 = cirq.LineQubit.range(2)
    theta, phi, lam = 0.3, 0.2, 0.1
    u3_matrix = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ])
    custom_gate = cirq.MatrixGate(u3_matrix)
    controlled_gate = custom_gate.controlled()
    circuit = cirq.Circuit(controlled_gate.on(q0, q1))
    return circuit
