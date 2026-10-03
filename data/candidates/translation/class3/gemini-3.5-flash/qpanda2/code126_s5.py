# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

# Create program and get unitary
prog = pq.QProg()
prog << pq.H(q[0])
u_list = machine.get_unitary_of_qprog(prog)

def calculate_phase_difference_fidelity():
    u = np.array(u_list).reshape((2, 2))
    op_a = u
    op_b = np.exp(1j * 0.5) * u
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / (d**2)
    return fidelity

# Manual cleanup
machine.finalize()
