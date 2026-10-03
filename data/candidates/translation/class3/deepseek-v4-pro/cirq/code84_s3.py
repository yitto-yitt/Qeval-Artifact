# EVAL_META: task_id=84, framework=cirq, class=3
import numpy as np
import cirq

def controlled_custom_unitary_circuit():
    theta = 0.3
    phi = 0.2
    lam = 0.1

    unitary = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (lam + phi)) * np.cos(theta / 2)]
    ])

    custom_gate = cirq.MatrixGate(unitary).controlled(1)

    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(custom_gate(q0, q1))

    return circuit
