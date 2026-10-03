# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, U3
from math import pi

def custom_rotation_gate():
    circuit = QCircuit()
    q = Qubit(0)
    circuit << U3(q, pi / 2, pi / 2, pi / 2)
    return circuit
