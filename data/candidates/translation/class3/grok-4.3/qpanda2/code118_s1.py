# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
def create_c3sx_circuit():
    prog = QProg()
    c3sx_mat = np.eye(16, dtype=complex)
    sx_mat = np.array([[0.5+0.5j, 0.5-0.5j], [0.5-0.5j, 0.5+0.5j]], dtype=complex)
    c3sx_mat[7, 7] = sx_mat[0, 0]
    c3sx_mat[7, 15] = sx_mat[0, 1]
    c3sx_mat[15, 7] = sx_mat[1, 0]
    c3sx_mat[15, 15] = sx_mat[1, 1]
    prog << QOracle(qubits, c3sx_mat)
    return prog
machine.finalize()
