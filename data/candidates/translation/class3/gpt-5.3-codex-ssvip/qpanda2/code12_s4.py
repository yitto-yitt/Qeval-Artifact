# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def get_unitary():
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    unitary = np.array(pq.get_matrix(prog), dtype=complex)
    return unitary

machine.finalize()
