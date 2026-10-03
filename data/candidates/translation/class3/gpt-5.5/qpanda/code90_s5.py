# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *


def create_custom_controlled():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(4)
    else:
        qubits = qvm.qalloc_many(4)

    custom = QCircuit()
    custom << X(qubits[1])
    custom << H(qubits[2])

    controls = [qubits[0], qubits[3]]
    if hasattr(custom, "set_control"):
        custom.set_control(controls)
    else:
        custom = custom.control(controls)

    prog = QProg()
    prog << custom

    create_custom_controlled._qvm = qvm
    create_custom_controlled._qubits = qubits
    return prog
