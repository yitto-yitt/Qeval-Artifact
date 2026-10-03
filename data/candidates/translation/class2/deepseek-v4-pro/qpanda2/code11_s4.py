# EVAL_META: task_id=11, framework=qpanda2, class=2
import numpy as np
from pyqpanda import init, CPUQVM, QProg, QCircuit

def get_statevector(circuit):
    init()
    qvm = CPUQVM()
    qvm.init()
    try:
        if isinstance(circuit, QCircuit):
            prog = QProg()
            prog << circuit
        else:
            prog = circuit
        qvm.directly_run(prog)
        state = qvm.get_qstate()
        return np.array(state, dtype=complex)
    finally:
        qvm.finalize()
