# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = pq.QProg()
    prog << pq.H(q[0])
    U = np.array(pq.get_matrix(prog), dtype=complex)
    V = np.exp(1j * 0.5) * U
    d = U.shape[0]
    fidelity = (np.abs(np.trace(np.conjugate(U.T) @ V)) ** 2) / (d ** 2)
    return float(np.real_if_close(fidelity))

machine.finalize()
