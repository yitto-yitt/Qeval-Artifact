# EVAL_META: task_id=84, framework=qpanda, class=3
import pyqpanda3.core as pq

def controlled_custom_unitary_circuit():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    
    # Define custom unitary matrix for U3(0.3, 0.2, 0.1)
    # U3 gate matrix: [[cos(theta/2), -e^{i*lambda}*sin(theta/2)], [e^{i*phi}*sin(theta/2), e^{i*(phi+lambda)}*cos(theta/2)]]
    import numpy as np
    theta = 0.3
    phi = 0.2
    lam = 0.1
    
    cos_half_theta = np.cos(theta / 2)
    sin_half_theta = np.sin(theta / 2)
    
    u_matrix = [
        [cos_half_theta, -np.exp(1j * lam) * sin_half_theta],
        [np.exp(1j * phi) * sin_half_theta, np.exp(1j * (phi + lam)) * cos_half_theta]
    ]
    
    # Apply controlled-U gate
    prog << pq.ControlledU(qubits[0], qubits[1], u_matrix)
    
    return prog, machine, qubits
