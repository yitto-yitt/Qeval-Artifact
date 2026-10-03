# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def apply_op_back():
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    return prog


atexit.register(machine.finalize)
