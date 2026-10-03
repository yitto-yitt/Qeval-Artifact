# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *

def create_operator():
    machine = CPUQVM()
    if hasattr(machine, "init"):
        machine.init()
    else:
        machine.init_qvm()

    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    prog = QProg()
    prog << X(qubits[0]) << X(qubits[1])

    global _QPANDA_TASK10_KEEPALIVE
    try:
        _QPANDA_TASK10_KEEPALIVE.append((machine, qubits, cbits))
    except NameError:
        _QPANDA_TASK10_KEEPALIVE = [(machine, qubits, cbits)]

    return prog
