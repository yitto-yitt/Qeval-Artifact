# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    u_matrix = np.array([
        [c, -np.exp(1j * lam) * s],
        [np.exp(1j * phi) * s, np.exp(1j * (phi + lam)) * c]
    ])
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.MatrixGate(u_matrix).on(qubit))
    return circuit
