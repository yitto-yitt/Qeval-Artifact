# EVAL_META: task_id=13, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, Qubit, U3

def custom_rotation_gate():
    circuit = QCircuit()
    q = Qubit(0)
    circuit << U3(q, math.pi / 2, math.pi / 2, math.pi / 2)
    return circuit
