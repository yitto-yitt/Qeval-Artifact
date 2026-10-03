# EVAL_META: task_id=90, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    custom = QCircuit()
    custom << X(q[1])
    custom << H(q[2])
    custom.set_control([q[0], q[3]])

    qc2 = QProg()
    qc2 << custom
    return qc2

atexit.register(machine.finalize)
