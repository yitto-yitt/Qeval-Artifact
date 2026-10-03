# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    cos = np.cos(theta / 2)
    sin = np.sin(theta / 2)
    matrix = np.array([
        [cos, -np.exp(1j * lam) * sin],
        [np.exp(1j * phi) * sin, np.exp(1j * (phi + lam)) * cos]
    ], dtype=complex)
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.MatrixGate(matrix).on(q))
    return circuit
