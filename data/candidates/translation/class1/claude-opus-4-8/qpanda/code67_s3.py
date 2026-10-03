# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import QCircuit, QProg, H, CNOT, RY, measure


def chsh_circuit(alice, bob):
    prog = QProg()
    circ = QCircuit()
    circ << H(0)
    circ << CNOT(0, 1)
    if alice == 0:
        circ << RY(0, 0)
    else:
        circ << RY(0, -pi / 2)
    if bob == 0:
        circ << RY(1, -pi / 4)
    else:
        circ << RY(1, pi / 4)
    prog << circ
    prog << measure(0, 0)
    prog << measure(1, 1)
    return prog
