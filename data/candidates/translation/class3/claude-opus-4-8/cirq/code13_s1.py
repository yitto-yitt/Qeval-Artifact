# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np


def custom_rotation_gate():
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    qubit = cirq.LineQubit(0)
    u = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)],
    ])
    gate = cirq.MatrixGate(u)
    circuit = cirq.Circuit()
    circuit.append(gate.on(qubit))
    return circuit
