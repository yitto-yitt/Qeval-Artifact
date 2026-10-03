# EVAL_META: task_id=11, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def get_statevector(circuit):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qprog = pq.QProg()
        qprog << circuit
        state = qvm.get_qstate()
        return np.array(state, dtype=complex)
    finally:
        qvm.finalize()
