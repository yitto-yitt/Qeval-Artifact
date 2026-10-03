# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, S, CNOT

def create_cy_gate():
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAllocMany(2)
    prog = QProg()
    prog << S(q[1]).dagger() << CNOT(q[0], q[1]) << S(q[1])
    return prog
