# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import QCircuit, Qubit, CBit, RY, CH, CNOT, X, measure


def w_state():
    circuit = QCircuit()
    q = [Qubit(i) for i in range(3)]
    c = [CBit(i) for i in range(3)]
    circuit << RY(q[0], 2 * arccos(1 / sqrt(3)))
    circuit << CH(q[0], q[1])
    circuit << CNOT(q[1], q[2])
    circuit << CNOT(q[0], q[1])
    circuit << X(q[0])
    circuit << measure(q[0], c[0])
    circuit << measure(q[1], c[1])
    circuit << measure(q[2], c[2])
    return circuit
