# EVAL_META: task_id=12, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def get_unitary():
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    mat = pq.get_matrix(prog)
    return np.array(mat)

machine.finalize()
