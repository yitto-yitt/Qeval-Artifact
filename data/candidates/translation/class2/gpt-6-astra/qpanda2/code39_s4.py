# EVAL_META: task_id=39, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def create_uniform_superposition(n):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(n)
        prog = pq.QProg()
        for qubit in qubits:
            prog << pq.H(qubit)
        qvm.directly_run(prog)
        return np.array(qvm.get_qstate(), dtype=complex)
    finally:
        qvm.finalize()
