# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    q0, q1 = cirq.LineQubit.range(2)
    theta = 0.3
    phi = 0.2
    lam = 0.1
    u = np.array(
        [
            [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
            [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)],
        ],
        dtype=complex,
    )
    gate = cirq.ControlledGate(cirq.MatrixGate(u))
    return cirq.Circuit(gate(q0, q1))
