# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def rx_gate(value=None):
    qc = QCircuit()
    theta = value if value is not None else "theta"
    qc.rx(theta, 0)
    return qc
