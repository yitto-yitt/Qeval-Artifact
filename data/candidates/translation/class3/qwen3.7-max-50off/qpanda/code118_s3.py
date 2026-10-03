# EVAL_META: task_id=118, framework=qpanda, class=3
import numpy as np
from pyqpanda3 import QuantumCircuit

def create_c3sx_circuit():
    qc = QuantumCircuit(4)
    sx = np.array([[1+1j, 1-1j], [1-1j, 1+1j]]) / 2
    mat = np.eye(16, dtype=complex)
    mat[14:16, 14:16] = sx
    qc.unitary(mat, [0, 1, 2, 3])
    return qc
