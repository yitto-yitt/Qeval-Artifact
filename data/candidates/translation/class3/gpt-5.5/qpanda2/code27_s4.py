# EVAL_META: task_id=27, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QProg, H, CNOT

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def apply_op_back():
    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(H(q[0]))
    return prog


atexit.register(machine.finalize)
