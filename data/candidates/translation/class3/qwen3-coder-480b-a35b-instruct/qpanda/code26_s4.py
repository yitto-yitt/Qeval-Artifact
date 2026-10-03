# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import *
from pyqpanda3.utils import *


def bell_dag():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    
    dag = circuit_to_dag(prog, qvm)
    return dag
