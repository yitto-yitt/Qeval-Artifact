# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *


def create_custom_controlled():
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(4)
    elif hasattr(machine, "qalloc_many"):
        q = machine.qalloc_many(4)
    else:
        q = list(range(4))

    controls = [q[0], q[3]]

    custom = QCircuit()
    custom << X(q[1])
    custom << H(q[2])
    custom.set_control(controls)

    qc2 = QProg()
    qc2 << custom

    create_custom_controlled._machine = machine
    return qc2
