# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)

    custom = QCircuit()
    custom << X(q[0]) << H(q[1])

    controlled_custom = custom.control([q[0], q[3]])

    prog = QProg()
    prog << controlled_custom

    return prog
