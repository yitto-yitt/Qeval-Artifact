# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, Unitary
import numpy as np

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qubits = [Qubit() for _ in range(n)]
    prog = QProg()
    mat = np.diag(diag).tolist()
    prog << Unitary(qubits, mat)
    return prog
