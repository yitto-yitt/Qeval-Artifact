# EVAL_META: task_id=67, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def chsh_circuit(alice, bob):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.CNOT(q[0], q[1])
    
    if alice == 0:
        prog << pq.RY(q[0], 0.0)
    else:
        prog << pq.RY(q[0], -np.pi / 2)
        
    prog << pq.Measure(q[0], c[0])
    
    if bob == 0:
        prog << pq.RY(q[1], -np.pi / 4)
    else:
        prog << pq.RY(q[1], np.pi / 4)
        
    prog << pq.Measure(q[1], c[1])
    
    return prog
