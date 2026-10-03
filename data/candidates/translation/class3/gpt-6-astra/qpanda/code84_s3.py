# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, U3


def controlled_custom_unitary_circuit():
    prog = QProg()
    prog << U3(1, 0.3, 0.2, 0.1).control([0])
    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
