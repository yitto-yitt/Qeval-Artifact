# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = pq.QProg()
    prog << pq.H(q[0])
    U = np.array(pq.get_unitary(prog), dtype=complex).reshape((2, 2))
    op_a = U
    op_b = np.exp(1j * 0.5) * U
    d = op_a.shape[0]
    fidelity = abs(np.trace(np.conjugate(op_a.T) @ op_b)) ** 2 / (d ** 2)
    return float(np.real_if_close(fidelity))

machine.finalize()
