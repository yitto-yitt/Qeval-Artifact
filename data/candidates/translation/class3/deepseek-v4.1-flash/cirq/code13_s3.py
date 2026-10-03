# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    U = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ])
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(U).on(q))
    return circuit
