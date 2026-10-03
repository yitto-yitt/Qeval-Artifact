# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *

def get_statevector(circuit):
    prog = QProg()
    prog.insert(circuit)
    directly_run(prog)
    return get_qstate()
