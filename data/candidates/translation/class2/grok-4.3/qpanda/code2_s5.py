# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import *

def create_bell_statevector():
    machine = CPUQVM()
    machine.initQVM()
    qvec = machine.qAllocMany(2)
    prog = QProg()
    prog << H(qvec[0]) << CNOT(qvec[0], qvec[1])
    machine.directlyRun(prog)
    result = machine.getQState()
    return result
