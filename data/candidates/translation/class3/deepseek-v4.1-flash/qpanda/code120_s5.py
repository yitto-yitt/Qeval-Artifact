# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np
import math

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    mat = np.diag(diag).astype(np.complex128)
    prog = QProg()
    qubits = prog.qAlloc(n)
    prog << QGate(mat, qubits)
    return prog
