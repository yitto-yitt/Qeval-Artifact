# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
from pyqpanda import QuantumCircuit, QMachineType, init


def w_state():
    init(QMachineType.CPU)
    circuit = QuantumCircuit(3)
    circuit.ry(2 * arccos(1 / sqrt(3)), 0)
    circuit.ch(0, 1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.x(0)
    circuit.measure_all()
    return circuit
