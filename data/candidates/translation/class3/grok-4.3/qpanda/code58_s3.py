# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import *
from numpy import pi

def create_ch_gate():
    circuit = QCircuit()
    q = [Qubit(i) for i in range(2)]
    circuit << RY(q[1], pi/4) << CNOT(q[0], q[1]) << RY(q[1], -pi/4)
    return circuit
