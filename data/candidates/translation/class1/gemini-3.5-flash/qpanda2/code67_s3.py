# EVAL_META: task_id=67, framework=qpanda2, class=1
from pyqpanda import *
import numpy as np

def chsh_circuit(alice, bob):
    try:
        init_quantum_share()
    except Exception:
        pass
    
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    prog = QProg()
    
    prog << H(q[0]) \
         << CNOT(q[0], q[1]) \
         << BARRIER(q)
         
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
