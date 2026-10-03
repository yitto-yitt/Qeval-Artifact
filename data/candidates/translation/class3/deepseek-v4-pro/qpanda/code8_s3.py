# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Parameter

def rx_gate(value=None):
    theta = Parameter("theta")
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    if value is not None:
        return qc.bind_parameters({theta: value})
    return qc
