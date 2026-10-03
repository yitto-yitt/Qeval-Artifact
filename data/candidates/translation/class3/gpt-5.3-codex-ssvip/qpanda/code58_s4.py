# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, CNOT
from math import pi

def create_ch_gate():
    circuit = QCircuit()
    circuit.insert(RY(1, pi / 4))
    circuit.insert(CNOT(0, 1))
    circuit.insert(RY(1, -pi / 4))
    return circuit
