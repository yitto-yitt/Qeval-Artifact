# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt, pi
from pyqpanda3.core import QProg, CPUQVM, RY, CNOT, X, measure


def w_state():
    circuit = QProg()
    circuit << RY(0, 2 * arccos(1 / sqrt(3)))
    circuit << RY(1, pi / 4)
    circuit << CNOT(0, 1)
    circuit << RY(1, -pi / 4)
    circuit << CNOT(1, 2)
    circuit << CNOT(0, 1)
    circuit << X(0)
    circuit << measure(0, 0)
    circuit << measure(1, 1)
    circuit << measure(2, 2)
    simulator = CPUQVM()
    simulator.run(circuit, 1)
    return circuit
