# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, I


def apply_op_back():
    prog = QProg()
    prog << I(2)
    prog << H(0)
    prog << CNOT(0, 1)
    prog << H(0)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
