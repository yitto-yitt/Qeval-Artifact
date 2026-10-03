# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)

    prog = QProg()
    prog << H(q[0])
    prog << CSWAP(q[0], q[1], q[2])
    prog << H(q[1])
    prog << Sdag(q[0]).control([q[1]])

    return prog
