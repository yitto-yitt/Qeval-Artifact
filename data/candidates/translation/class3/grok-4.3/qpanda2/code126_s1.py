# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
def calculate_phase_difference_fidelity():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    op_a = pq.get_unitary_matrix(prog)
    phase = np.exp(1j * 0.5)
    op_b = phase * op_a
    d = op_a.shape[0]
    fidelity = (np.abs(np.trace(np.dot(np.conjugate(op_a).T, op_b))) / d) ** 2
    return fidelity
machine.finalize()
