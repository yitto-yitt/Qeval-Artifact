# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    prog = QProg()
    prog << circuit
    state = qvm.get_qstate(prog)
    qvm.finalize()
    return state
