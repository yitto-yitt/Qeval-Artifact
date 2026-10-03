# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    q = cirq.LineQubit.range(2)
    theta, phi, lam = 0.3, 0.2, 0.1
    custom_unitary = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ], dtype=complex)
    custom_gate = cirq.MatrixGate(custom_unitary)
    controlled_gate = custom_gate.controlled(num_controls=1)
    circuit = cirq.Circuit()
    circuit.append(controlled_gate.on(q[0], q[1]))
    return circuit
