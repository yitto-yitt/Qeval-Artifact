# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc, RX, Var

def rx_gate(value=None):
    q = qAlloc(1)
    circuit = QCircuit()
    if value is not None:
        circuit << RX(q[0], value)
    else:
        circuit << RX(q[0], Var("theta"))
    return circuit
