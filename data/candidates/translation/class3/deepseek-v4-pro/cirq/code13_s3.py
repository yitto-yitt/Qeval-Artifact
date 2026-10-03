# EVAL_META: task_id=13, framework=cirq, class=3
import numpy as np
import cirq

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2

    u = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ])

    gate = cirq.MatrixGate(u)
    return cirq.Circuit(gate.on(q))
