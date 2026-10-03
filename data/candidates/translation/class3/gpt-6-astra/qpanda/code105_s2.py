# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT, T


def initialize_cnot_dihedral():
    prog = QProg()
    prog << CNOT(0, 1) << T(0)
    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
