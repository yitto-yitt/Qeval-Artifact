# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    # U gate with theta=pi/2, phi=pi/2, lambda=pi/2
    # U(theta, phi, lambda) = Rz(phi) * Ry(theta) * Rz(lambda)
    circuit.append([
        cirq.rz(np.pi/2).on(qubit),
        cirq.ry(np.pi/2).on(qubit),
        cirq.rz(np.pi/2).on(qubit)
    ])
    
    return circuit
