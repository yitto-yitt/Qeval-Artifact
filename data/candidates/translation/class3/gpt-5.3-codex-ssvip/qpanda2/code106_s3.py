# EVAL_META: task_id=106, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    prog1 = pq.QProg()
    prog1 << pq.CNOT(q[0], q[1]) << pq.T(q[0])

    prog2 = pq.QProg()
    prog2 << pq.CNOT(q[0], q[1]) << pq.T(q[0]) << pq.X(q[1])

    u1 = np.array(pq.get_unitary(prog1, False), dtype=complex)
    u2 = np.array(pq.get_unitary(prog2, False), dtype=complex)

    composed_elem = u1 @ u2
    machine.finalize()
    return composed_elem
