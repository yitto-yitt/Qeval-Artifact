# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, CNOT
from numpy import pi

def create_ch_gate():
    circuit = QCircuit()
    circuit << RY(1, pi/4) << CNOT(0, 1) << RY(1, -pi/4)
    return circuit
