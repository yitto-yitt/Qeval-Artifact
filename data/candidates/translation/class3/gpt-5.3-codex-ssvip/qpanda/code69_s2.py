# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << S(q[1]).control([q[0]])
    prog << H(q[1])
    prog << Sdag(q[0]).control([q[1]])

    return prog
