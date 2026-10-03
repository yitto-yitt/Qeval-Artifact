# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    prog = QProg()
    if value is not None:
        prog << RX(qubits[0], value)
    else:
        prog << RX(qubits[0], 0)
    return prog

machine.finalize()
