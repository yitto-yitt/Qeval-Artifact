# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def apply_op_back():
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    dag = qprog_to_dag(prog)
    return dag


machine.finalize()
