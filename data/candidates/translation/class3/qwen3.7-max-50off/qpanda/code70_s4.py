# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3 import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = QuantumMachine()
    q = qvm.qAlloc_many(3)
    prog = QProg()
    
    prog << H(q[0])
    prog << CSWAP(q[0], q[1], q[2])
    prog << H(q[1])
    prog << CS(q[1], q[0]).dag()
    
    return prog
