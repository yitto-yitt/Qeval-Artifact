# EVAL_META: task_id=60, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, RZ, CNOT

def create_cy_gate():
    circuit = QProg()
    circuit << RZ(1, -pi / 2)
    circuit << CNOT(0, 1)
    circuit << RZ(1, pi / 2)
    return circuit
