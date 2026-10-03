# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3 import *

def rx_gate(value=None):
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(1)
    circ = QCircuit()
    if value is not None:
        circ << RX(q[0], value)
    else:
        circ << RX(q[0], 0.0)
    return circ
