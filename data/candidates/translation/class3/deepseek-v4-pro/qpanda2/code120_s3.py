# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    if 2 ** n != len(diag):
        raise ValueError("The diagonal size has to be a power of 2.")
    if n == 0:
        return QCircuit()
    q = machine.qAlloc_many(n)
    matrix = np.diag(np.asarray(diag, dtype=complex)).tolist()
    circuit = QCircuit()
    circuit << QOracle(q, matrix)
    return circuit

machine.finalize()
