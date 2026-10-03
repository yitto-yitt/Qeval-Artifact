# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init()
    prog = QProg()
    prog << circuit
    qvm.directlyRun(prog)
    return qvm.getQState()
