# EVAL_META: task_id=39, framework=qpanda2, class=2
import numpy as np
from pyqpanda import CPUQVM, QCircuit, H

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QCircuit()
    for i in range(n):
        prog << H(qubits[i])
    qvm.directly_run(prog)
    state = qvm.get_qstate()
    result = np.array(state, dtype=complex)
    qvm.finalize()
    return result
