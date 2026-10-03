# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    circuit = cirq.Circuit()
    q = cirq.LineQubit(0)
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    mat = np.array([
        [c, -np.exp(1j * lam) * s],
        [np.exp(1j * phi) * s, np.exp(1j * (phi + lam)) * c]
    ], dtype=complex)
    gate = cirq.MatrixGate(mat)
    circuit.append(gate.on(q))
    return circuit
