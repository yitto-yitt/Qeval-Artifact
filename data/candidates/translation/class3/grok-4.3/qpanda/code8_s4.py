# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import Parameter, QCircuit, RX

def rx_gate(value=None):
    theta = Parameter("theta")
    qcircuit = QCircuit()
    qcircuit << RX(0, theta)
    if value is not None:
        return qcircuit.assign_parameters({theta: value})
    return qcircuit
