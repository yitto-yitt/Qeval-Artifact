# EVAL_META: task_id=84, framework=cirq, class=3
import numpy as np
import cirq

def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    u = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ])
    gate = cirq.MatrixGate(u)
    controlled_gate = gate.controlled()
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(controlled_gate(q0, q1))
    return circuit
