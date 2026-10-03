# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)

    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CRZ(q[0], q[1], theta))
    prog.insert(H(q[1]))
    prog.insert(CRY(q[1], q[0], theta))

    return prog
