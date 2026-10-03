# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, I, measure


def bell_dag():
    prog = QProg()
    prog << I(2)
    prog << H(0)
    prog << CNOT(0, 1)
    prog << measure(0, 0)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
