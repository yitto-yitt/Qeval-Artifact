# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from scipy.linalg import cossin
from pyqpanda3.core import QProg, QuantumMachine, CNOT, RZ, RY

def u2_to_params(W):
    alpha = np.angle(np.linalg.det(W)) / 2
    SU = W * np.exp(-1j * alpha)
    a = SU[0, 0]
    b = SU[1, 0]
    gamma = 2 * np.arccos(np.clip(np.abs(a), 0, 1))
    angle_a = np.angle(a) if np.abs(a) > 1e-10 else 0
    angle_b = np.angle(b) if np.abs(b) > 1e-10 else 0
    beta = -angle_a + angle_b
    delta = -angle_a - angle_b
    return alpha, beta, gamma, delta

def decompose_unitary(unitary):
    U = np.array(unitary, dtype=complex)
    U1, U2, theta, V1, V2 = cossin(U, p=2, q=2)
    
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = QProg()
    
    def add_multiplexed_u2(prog, W1, W2, control, target):
        a1, b1, g1, d1 = u2_to_params(W1)
        a2, b2, g2, d2 = u2_to_params(W2)
        
        prog << RZ(control, a2 - a1)
        
        prog << RZ(target, (b1 + b2) / 2)
        prog << CNOT(control, target)
        prog << RZ(target, (b1 - b2) / 2)
        prog << CNOT(control, target)
        
        prog << RY(target, (g1 + g2) / 2)
        prog << CNOT(control, target)
        prog << RY(target, (g1 - g2) / 2)
        prog << CNOT(control, target)
        
        prog << RZ(target, (d1 + d2) / 2)
        prog << CNOT(control, target)
        prog << RZ(target, (d1 - d2) / 2)
        prog << CNOT(control, target)

    add_multiplexed_u2(prog, V1, V2, q[0], q[1])
    
    t1, t2 = theta[0], theta[1]
    prog << RY(q[1], t1 + t2)
    prog << CNOT(q[0], q[1])
    prog << RY(q[1], t1 - t2)
    prog << CNOT(q[0], q[1])
    
    add_multiplexed_u2(prog, U1, U2, q[0], q[1])
    
    return prog
