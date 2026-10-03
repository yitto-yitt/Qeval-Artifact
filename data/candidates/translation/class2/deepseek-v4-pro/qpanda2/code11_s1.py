# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init()
    if isinstance(circuit, QProg):
        prog = circuit
    else:
        prog = QProg()
        prog << circuit
    qvm.directlyRun(prog)
    return qvm.getQState()
