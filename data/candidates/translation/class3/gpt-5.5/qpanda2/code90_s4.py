# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    prog = QProg()
    custom = QCircuit()
    custom << X(q[1])
    custom << H(q[2])
    prog << custom.control([q[0], q[3]])
    return prog

atexit.register(machine.finalize)
