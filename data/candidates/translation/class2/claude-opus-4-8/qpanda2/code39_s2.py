# EVAL_META: task_id=39, framework=qpanda2, class=2
import numpy as np
from pyqpanda import CPUQVM, QCircuit, H

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QCircuit()
    for q in qubits:
        prog << H(q)
    qvm.directly_run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return np.array(state)
