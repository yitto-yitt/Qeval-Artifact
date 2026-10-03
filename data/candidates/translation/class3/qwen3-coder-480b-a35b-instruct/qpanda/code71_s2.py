# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_csx01_h1():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    
    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CS(q[0], q[1]))  # CS gate as controlled-SX equivalent
    prog.insert(H(q[1]))
    
    return prog
