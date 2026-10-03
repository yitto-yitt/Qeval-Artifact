# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT, T, X


def compose_cnot_dihedral():
    composed = QProg()
    composed << CNOT(0, 1) << T(0)
    composed << CNOT(0, 1) << T(0) << X(1)

    simulator = CPUQVM()
    simulator.run(composed, 1)
    return composed
