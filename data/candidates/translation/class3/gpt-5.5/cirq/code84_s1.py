# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np


def controlled_custom_unitary_circuit():
    q0, q1 = cirq.LineQubit.range(2)

    theta = 0.3
    phi = 0.2
    lam = 0.1

    custom_unitary = np.array(
        [
            [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
            [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)],
        ],
        dtype=complex,
    )

    custom_gate = cirq.MatrixGate(custom_unitary)
    circuit = cirq.Circuit(custom_gate.on(q1).controlled_by(q0))
    return circuit
