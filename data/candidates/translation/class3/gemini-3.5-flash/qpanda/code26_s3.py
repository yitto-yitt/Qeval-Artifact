# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import *


def bell_dag():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(3)
    c = machine.cAllocMany(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    dag = qprog_to_dag(prog)
    return dag
