# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *
def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    prog = QProg()
    prog << circuit
    qvm.directly_run(prog)
    sv = qvm.get_qstate()
    return sv
