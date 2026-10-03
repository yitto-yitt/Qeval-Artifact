# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3 import QCircuit, RY, CNOT
import numpy as np

def create_ch_gate():
    circuit = QCircuit()
    q = circuit.qAlloc(2)
    circuit << RY(q[1], np.pi/4)
    circuit << CNOT(q[0], q[1])
    circuit << RY(q[1], -np.pi/4)
    return circuit
