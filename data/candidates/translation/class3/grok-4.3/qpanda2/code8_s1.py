# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
def rx_gate(value=None):
    circuit = QCircuit()
    theta = 0.0
    if value is not None:
        theta = value
    circuit << RX(q[0], theta)
    return circuit
machine.finalize()
