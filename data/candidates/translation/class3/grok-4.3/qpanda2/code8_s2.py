# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(1)

def rx_gate(value=None):
    quantum_circuit = QCircuit()
    if value is None:
        theta = var("theta")
        quantum_circuit << RX(q[0], theta)
    else:
        quantum_circuit << RX(q[0], value)
    return quantum_circuit

machine.finalize()
