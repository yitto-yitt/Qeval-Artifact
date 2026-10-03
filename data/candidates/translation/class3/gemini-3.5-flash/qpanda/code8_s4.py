# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, RX, var

def rx_gate(value=None):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    circuit = QCircuit()
    if value is None:
        theta = var(0.0)
        circuit << RX(q[0], theta)
    else:
        circuit << RX(q[0], value)
    return circuit
