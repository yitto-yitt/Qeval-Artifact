# EVAL_META: task_id=67, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3 import *
import math


def chsh_circuit(alice, bob):
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(BARRIER([q[0], q[1]]))
    
    if alice == 0:
        prog.insert(RY(0, q[0]))
    else:
        prog.insert(RY(-math.pi / 2, q[0]))
    
    prog.insert(Measure(q[0], c[0]))
    
    if bob == 0:
        prog.insert(RY(-math.pi / 4, q[1]))
    else:
        prog.insert(RY(math.pi / 4, q[1]))
    
    prog.insert(Measure(q[1], c[1]))
    
    # Extract circuit-like structure (though pyqpanda doesn't have exact circuit equivalent)
    # Return the program which represents the quantum operations
    return prog
