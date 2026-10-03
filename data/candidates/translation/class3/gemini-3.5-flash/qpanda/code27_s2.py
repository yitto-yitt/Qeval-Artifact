# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import *


def apply_op_back():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    dag = qprog_to_dag(prog)
    return dag
