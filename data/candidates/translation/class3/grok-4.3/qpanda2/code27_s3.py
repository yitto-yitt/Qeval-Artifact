# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(3)
def apply_op_back():
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << H(q[0])
    return prog
machine.finalize()
