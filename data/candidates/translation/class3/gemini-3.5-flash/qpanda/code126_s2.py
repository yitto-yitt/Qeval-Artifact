# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    prog = pq.QProg()
    prog << pq.H(qubits[0])

    matrix_list = pq.get_matrix(prog)
    op_a = np.array(matrix_list).reshape(2, 2)
    op_b = np.exp(1j * 0.5) * op_a

    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (d**2)
    return fidelity
