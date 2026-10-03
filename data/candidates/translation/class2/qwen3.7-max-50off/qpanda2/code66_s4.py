# EVAL_META: task_id=66, framework=qpanda2, class=2
import numpy as np
from pyqpanda import *

def w_state():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = QProg()
    
    theta = 2 * np.arccos(1 / np.sqrt(3))
    prog << RY(q[0], theta)
    prog << H(q[1]).control(q[0])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    
    for i in range(3):
        prog << Measure(q[i], c[i])
        
    return prog
