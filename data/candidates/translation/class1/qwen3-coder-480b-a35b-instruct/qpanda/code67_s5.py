# EVAL_META: task_id=67, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *
from math import pi


def chsh_circuit(alice, bob):
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << Barrier()
    
    if alice == 0:
        prog << RY(0, q[0])
    else:
        prog << RY(-pi / 2, q[0])
    
    prog << Measure(q[0], c[0])
    
    if bob == 0:
        prog << RY(-pi / 4, q[1])
    else:
        prog << RY(pi / 4, q[1])
    
    prog << Measure(q[1], c[1])
    
    return prog
