# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2

    c = np.cos(theta / 2)
    s = np.sin(theta / 2)

    matrix = np.array([
        [c, -s * np.exp(1j * lam)],
        [s * np.exp(1j * phi), c * np.exp(1j * (phi + lam))]
    ])

    q = cirq.LineQubit(0)
    return cirq.Circuit(cirq.MatrixGate(matrix)(q))
