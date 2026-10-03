# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    theta = phi = lam = np.pi / 2
    matrix = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2),
         np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ], dtype=complex)
    return cirq.Circuit(cirq.MatrixGate(matrix).on(cirq.LineQubit(0)))
