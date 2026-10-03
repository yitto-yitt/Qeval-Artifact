# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *
def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    qvm.directly_run(circuit)
    sv = qvm.get_qstate()
    return sv
