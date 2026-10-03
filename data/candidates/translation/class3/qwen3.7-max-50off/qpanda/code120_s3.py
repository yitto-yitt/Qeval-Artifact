# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, Qubit, Unitary

def create_diagonal_circuit(diag):
    n = int(np.round(np.log2(len(diag))))
    qubits = [Qubit() for _ in range(n)]
    mat = np.diag(diag).tolist()
    prog = QProg()
    prog << Unitary(mat, qubits)
    return prog
