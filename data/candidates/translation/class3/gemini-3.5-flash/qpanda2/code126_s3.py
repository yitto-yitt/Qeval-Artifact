# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

prog = pq.QProg()
prog << pq.H(q[0])
mat_list = pq.get_matrix(prog)

def calculate_phase_difference_fidelity():
    op_a = np.array(mat_list).reshape(2, 2)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    trace_val = np.trace(op_a.conj().T @ op_b)
    fidelity = np.abs(trace_val)**2 / (d**2)
    return fidelity

machine.finalize()
