# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, QProg, CNOT, T, X


def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(0, 1) << T(0)

    circ2 = QCircuit()
    circ2 << CNOT(0, 1) << T(0) << X(1)

    composed = QProg()
    composed << circ1 << circ2

    simulator = CPUQVM()
    simulator.run(composed, 1)
    return composed
