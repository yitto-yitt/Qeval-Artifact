# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RX, Variational

def rx_gate(value=None):
    theta = Variational("theta")
    circuit = QCircuit()
    if value is None:
        circuit << RX(0, theta)
    else:
        circuit << RX(0, value)
    return circuit
