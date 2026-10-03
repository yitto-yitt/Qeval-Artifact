# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import *

def rx_gate(value=None):
    circuit = QCircuit()
    q = Qubit(0)
    if value is not None:
        circuit << RX(q, value)
    else:
        theta = Var("theta")
        circuit << RX(q, theta)
    return circuit
