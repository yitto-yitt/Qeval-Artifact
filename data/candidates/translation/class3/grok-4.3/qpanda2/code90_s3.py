# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
def create_custom_controlled():
    prog = QProg()
    sub_circ = QCircuit()
    sub_circ << X(q[1]) << H(q[2])
    controlled_sub = sub_circ.control([q[0], q[3]])
    prog << controlled_sub
    return prog
machine.finalize()
