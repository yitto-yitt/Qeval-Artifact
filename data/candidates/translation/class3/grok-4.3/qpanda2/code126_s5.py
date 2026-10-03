# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog_a = pq.QProg()
    prog_a << pq.H(qubits[0])
    mat_a = pq.get_matrix(prog_a)
    phase = np.exp(1j * 0.5)
    mat_b = phase * mat_a
    d = mat_a.shape[0]
    trace_val = np.trace(np.dot(np.conj(mat_a).T, mat_b))
    fidelity = np.abs(trace_val / d) ** 2
    return fidelity

machine.finalize()
