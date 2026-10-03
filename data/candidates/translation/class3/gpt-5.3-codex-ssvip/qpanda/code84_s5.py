# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import *

def controlled_custom_unitary_circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)

    prog = QProg()
    prog.insert(CU(q[0], q[1], 0.3, 0.2, 0.1, 0.0))

    return prog
