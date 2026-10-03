# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    custom = QCircuit()
    custom << X(q[1]) << H(q[2])
    if hasattr(custom, "control"):
        return custom.control([q[0], q[3]])
    elif hasattr(custom, "set_control"):
        custom.set_control([q[0], q[3]])
        return custom
    elif hasattr(custom, "setControl"):
        custom.setControl([q[0], q[3]])
        return custom
    else:
        raise AttributeError("QCircuit control method not found")

machine.finalize()
