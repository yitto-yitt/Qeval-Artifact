# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def rx_gate(value=None):
    circuit = QCircuit()
    if value is None:
        theta = var("theta")
        circuit << RX(q[0], theta)
    else:
        circuit << RX(q[0], value)
    return circuit

machine.finalize()
