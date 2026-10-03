# EVAL_META: task_id=66, framework=qpanda2, class=2
import pyqpanda as pq
from numpy import arccos, sqrt

def w_state():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    angle = 2 * arccos(1 / sqrt(3))
    
    prog << pq.RY(q[0], angle)
    prog << pq.H(q[1]).control(q[0])
    prog << pq.CNOT(q[1], q[2])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.X(q[0])
    
    for i in range(3):
        prog << pq.Measure(q[i], c[i])
        
    return prog
