# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, CNOT, T


def initialize_cnot_dihedral():
    elem = QCircuit()
    elem << CNOT(0, 1) << T(0)
    prog = QProg()
    prog << elem
    qvm = CPUQVM()
    qvm.run(prog, 1)
    return elem
