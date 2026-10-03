# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, Var, RX

def rx_gate(value=None):
    qc = QCircuit()
    q = Qubit()
    theta = value if value is not None else Var("theta")
    qc << RX(q, theta)
    return qc
