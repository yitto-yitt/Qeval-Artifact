# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def compose_op():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    op = np.eye(2**3, dtype=complex)
    yx = np.kron(Y, X)
    full = np.kron(np.kron(Y, I), X)
    prog = pq.QProg()
    machine.directly_run(prog)
    return full

machine.finalize()
