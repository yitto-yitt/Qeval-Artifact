# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

# Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

atexit.register(machine.finalize)


def get_unitary():
    prog = pq.QProg()
    prog << pq.H(q[1]) << pq.CNOT(q[1], q[0])
    u = pq.get_unitary_matrix(prog)
    return np.array(u).reshape(4, 4)
