# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CS(q[0], q[1]) << H(q[1]) << CSdag(q[1], q[0])
    return prog
