# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit
import math

def create_ch_gate():
    circuit = QCircuit()
    circuit.ry(1, math.pi / 4)
    circuit.cnot(0, 1)
    circuit.ry(1, -math.pi / 4)
    return circuit
