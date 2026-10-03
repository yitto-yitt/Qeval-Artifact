# EVAL_META: task_id=11, framework=qpanda2, class=2
import numpy as np
from pyqpanda import CPUQVM, QProg

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()

    if isinstance(circuit, QProg):
        prog = circuit
    else:
        prog = QProg()
        prog << circuit

    qvm.directly_run(prog)
    sv = qvm.get_qstate()
    qvm.finalize()
    return np.array(sv)
