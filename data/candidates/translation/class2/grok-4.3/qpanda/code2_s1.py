# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def create_bell_statevector():
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAllocMany(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    qvm.directlyRun(prog)
    return qvm.getQState()
