# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    theta = 0.3
    phi = 0.2
    lam = 0.1

    u = np.array(
        [
            [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
            [
                np.exp(1j * phi) * np.sin(theta / 2),
                np.exp(1j * (phi + lam)) * np.cos(theta / 2),
            ],
        ],
        dtype=complex,
    )

    custom_gate = cirq.MatrixGate(u)
    controlled_gate = cirq.ControlledGate(custom_gate)

    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(controlled_gate.on(q0, q1))
