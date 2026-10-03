# EVAL_META: task_id=84, framework=cirq, class=3
import numpy as np
import cirq

def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    cos = np.cos(theta / 2)
    sin = np.sin(theta / 2)
    u = np.array([
        [cos, -np.exp(1j * lam) * sin],
        [np.exp(1j * phi) * sin, np.exp(1j * (phi + lam)) * cos]
    ], dtype=np.complex128)
    
    q0, q1 = cirq.LineQubit.range(2)
    gate = cirq.MatrixGate(u).controlled()
    
    return cirq.Circuit(gate(q0, q1))
