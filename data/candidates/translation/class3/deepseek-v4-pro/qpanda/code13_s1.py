# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, U3
import math

def custom_rotation_gate():
    circuit = QCircuit(1)
    circuit.insert(U3(0, math.pi / 2, math.pi / 2, math.pi / 2))
    return circuit
