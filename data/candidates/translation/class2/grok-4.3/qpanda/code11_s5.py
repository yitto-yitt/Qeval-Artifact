# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    qvm.directly_run(circuit)
    return qvm.get_qstate()
