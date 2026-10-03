# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, CNOT, Qubit
import numpy as np

def create_ch_gate():
    circuit = QCircuit()
    q0 = Qubit()
    q1 = Qubit()
    circuit << RY(q1, np.pi/4)
    circuit << CNOT(q0, q1)
    circuit << RY(q1, -np.pi/4)
    return circuit
