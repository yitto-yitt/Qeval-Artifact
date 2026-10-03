# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    u_matrix = np.array([
        [c, -np.exp(1j * lam) * s],
        [np.exp(1j * phi) * s, np.exp(1j * (phi + lam)) * c]
    ], dtype=complex)
    gate = cirq.MatrixGate(u_matrix)
    controlled_gate = cirq.ControlledGate(gate, num_controls=1)
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(controlled_gate(q0, q1))
    return circuit
