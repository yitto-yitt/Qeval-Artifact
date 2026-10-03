# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = pq.QProg()
    prog << pq.H(q[0])
    U = np.array(pq.get_unitary(prog), dtype=complex)
    dim = U.shape[0]
    phase = np.exp(1j * 0.5)
    V = phase * U
    fidelity = (np.abs(np.trace(np.conjugate(U.T) @ V)) ** 2) / (dim ** 2)
    return float(np.real_if_close(fidelity))

machine.finalize()
