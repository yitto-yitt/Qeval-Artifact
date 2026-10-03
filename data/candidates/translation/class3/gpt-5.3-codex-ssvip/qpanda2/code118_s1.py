# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = QProg()
    # Decomposition of C3SX (3-controlled SX) using MCX and single-qubit gates
    prog << H(q[3])
    prog << S(q[3])
    prog << X(q[3]).control([q[0], q[1], q[2]])
    prog << SDG(q[3])
    prog << H(q[3])
    return prog

machine.finalize()
