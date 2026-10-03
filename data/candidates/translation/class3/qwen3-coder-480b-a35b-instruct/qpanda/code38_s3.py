# EVAL_META: task_id=38, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CRZ(q[0], q[1], theta))
    prog.insert(pq.H(q[1]))
    prog.insert(pq.CRY(q[1], q[0], theta))
    
    return prog
