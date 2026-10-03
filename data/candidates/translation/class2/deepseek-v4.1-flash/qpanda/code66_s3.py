# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *


def w_state():
    circuit = QCircuit()
    angle = 2 * arccos(1 / sqrt(3))
    circuit << RY(0, angle)
    circuit << CH(0, 1)
    circuit << CNOT(1, 2)
    circuit << CNOT(0, 1)
    circuit << X(0)
    circuit << Measure(0, 0)
    circuit << Measure(1, 1)
    circuit << Measure(2, 2)
    return circuit
