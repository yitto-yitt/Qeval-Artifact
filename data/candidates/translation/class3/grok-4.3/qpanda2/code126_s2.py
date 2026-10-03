# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(qubits[0])
    mat_list = get_unitary_matrix(prog)
    op_a = np.array(mat_list, dtype=complex)
    op_b = np.exp(1j * 0.5) * op_a
    d = 2
    u_dag_v = np.dot(np.conjugate(op_a).T, op_b)
    trace_val = np.trace(u_dag_v)
    fidelity = (np.abs(trace_val) ** 2) / (d ** 2)
    return fidelity
machine.finalize()
