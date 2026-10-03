# EVAL_META: task_id=67, framework=qpanda, class=1
import numpy as np
from pyqpanda3 import *

def chsh_circuit(alice, bob):
    q = qAlloc(2)
    c = cAlloc(2)
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    
    if alice == 0:
        prog << RY(q[0], 0.0)
    else:
        prog << RY(q[0], -np.pi / 2)
        
    prog << Measure(q[0], c[0])
    
    if bob == 0:
        prog << RY(q[1], -np.pi / 4)
    else:
        prog << RY(q[1], np.pi / 4)
        
    prog << Measure(q[1], c[1])
    
    return prog
