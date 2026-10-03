# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RX, Parameter

def rx_gate(value=None):
    theta = Parameter("theta")
    q = Qubit()
    qc = QCircuit()
    qc << RX(q, theta)
    if value is not None:
        if hasattr(qc, 'assign_parameters'):
            bound = qc.assign_parameters({theta: value})
            if bound is not None:
                return bound
        try:
            theta.set_value(value)
        except AttributeError:
            theta.setValue(value)
    return qc
