# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubit = machine.qAlloc_many(1)

def rx_gate(value=None):
    circuit = QCircuit()
    if value is not None:
        circuit << RX(qubit[0], value)
    else:
        circuit << RX(qubit[0], 0.0)
    return circuit

atexit.register(machine.finalize)
