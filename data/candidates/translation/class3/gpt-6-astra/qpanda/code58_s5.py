# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QProg, RY, CNOT
from numpy import pi

def create_ch_gate():
    circuit = QProg()
    circuit << RY(1, pi / 4)
    circuit << CNOT(0, 1)
    circuit << RY(1, -pi / 4)
    return circuit
