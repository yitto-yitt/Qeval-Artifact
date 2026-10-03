# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import QCircuit, QProg, H, CNOT, RY, measure


def chsh_circuit(alice, bob):
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)
    if alice == 0:
        qc << RY(0, 0)
    else:
        qc << RY(0, -pi / 2)
    if bob == 0:
        qc << RY(1, -pi / 4)
    else:
        qc << RY(1, pi / 4)

    prog = QProg()
    prog << qc
    prog << measure(0, 0)
    prog << measure(1, 1)
    return prog
