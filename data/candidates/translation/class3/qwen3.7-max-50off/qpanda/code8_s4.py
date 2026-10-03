# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Parameter

def rx_gate(value=None):
    theta = Parameter("theta")
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    if value is not None:
        qc_bound = QuantumCircuit(1)
        qc_bound.rx(value, 0)
        return qc_bound
    return qc
