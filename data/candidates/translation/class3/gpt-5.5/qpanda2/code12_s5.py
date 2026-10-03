# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qbits = machine.qAlloc_many(2)
_ = atexit.register(lambda: machine.finalize())


def get_unitary():
    def as_square_matrix(value):
        mat = np.asarray(value, dtype=complex)
        if mat.ndim == 1:
            dim = int(round(np.sqrt(mat.size)))
            mat = mat.reshape((dim, dim))
        return mat

    def framework_matrix(program):
        try:
            return as_square_matrix(pq.get_matrix(program))
        except Exception:
            return as_square_matrix(pq.get_unitary(program))

    prog = pq.QProg()
    prog << pq.H(qbits[0])
    prog << pq.CNOT(qbits[0], qbits[1])
    raw = framework_matrix(prog)

    cal0 = pq.QProg()
    cal0 << pq.CNOT(qbits[0], qbits[1])
    cal0 << pq.CNOT(qbits[0], qbits[1])
    cal0 << pq.X(qbits[0])

    cal1 = pq.QProg()
    cal1 << pq.CNOT(qbits[0], qbits[1])
    cal1 << pq.CNOT(qbits[0], qbits[1])
    cal1 << pq.X(qbits[1])

    m0 = framework_matrix(cal0)
    m1 = framework_matrix(cal1)

    p0 = int(np.argmax(np.abs(m0[:, 0])))
    p1 = int(np.argmax(np.abs(m1[:, 0])))

    def logical_index(raw_index):
        return (1 if (raw_index & p0) else 0) | (2 if (raw_index & p1) else 0)

    unitary = np.zeros_like(raw, dtype=complex)
    for r_out in range(raw.shape[0]):
        for r_in in range(raw.shape[1]):
            unitary[logical_index(r_out), logical_index(r_in)] = raw[r_out, r_in]

    return unitary
