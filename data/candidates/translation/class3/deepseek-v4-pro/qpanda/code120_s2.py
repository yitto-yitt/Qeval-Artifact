# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumCircuit

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qc = QuantumCircuit(n)
    qc.oracle(np.diag(diag), list(range(n)))
    return qc
