# EVAL_META: task_id=66, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QProg, QVec, CVec, RY, CX, X, Measure

def w_state():
    q = QVec(3)
    c = CVec(3)
    prog = QProg()
    
    theta = 2 * np.arccos(1 / np.sqrt(3))
    prog << RY(q[0], theta)
    
    prog << RY(q[1], -np.pi/4)
    prog << CX(q[0], q[1])
    prog << RY(q[1], np.pi/4)
    
    prog << CX(q[1], q[2])
    prog << CX(q[0], q[1])
    prog << X(q[0])
    
    for i in range(3):
        prog << Measure(q[i], c[i])
        
    return prog
