# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def rx_gate(value=None):
    circuit = QCircuit()
    theta = value if value is not None else 0.0
    circuit << RX(q[0], theta)
    return circuit

machine.finalize()
