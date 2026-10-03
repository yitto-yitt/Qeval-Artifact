# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda import *
import numpy as np

def custom_rotation_gate():
    machine = init(QMachineType.CPU)
    prog = QProg()
    qubits = machine.qAlloc_many(1)
    cbits = machine.cAlloc_many(1)
    
    # Create U gate with theta=pi/2, phi=pi/2, lambda=pi/2
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    
    # U gate in QPanda is defined as U(theta, phi, lambda)
    prog.insert(U(qubits[0], theta, phi, lam))
    
    return prog
