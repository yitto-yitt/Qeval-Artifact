# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CPUQVM, CNOT, T, X


def compose_cnot_dihedral():
    circ = QCircuit(2)
    circ << CNOT(0, 1)
    circ << T(0)
    circ << CNOT(0, 1)
    circ << T(0)
    circ << X(1)

    prog = QProg()
    prog << circ

    qvm = CPUQVM()
    qvm.run(prog, 1000)
    result = qvm.result().get_counts()
    return result
