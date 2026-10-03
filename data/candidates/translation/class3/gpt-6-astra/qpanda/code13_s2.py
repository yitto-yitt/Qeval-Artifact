# EVAL_META: task_id=13, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, U3

def custom_rotation_gate():
    circuit = QProg()
    circuit << U3(0, pi / 2, pi / 2, pi / 2)
    return circuit
