# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda import QOracle
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    if 2 ** n != len(diag):
        raise ValueError("diag length must be a power of 2")
    if n == 0:
        return QCircuit()
    if n > len(qubits):
        raise ValueError("Not enough globally allocated qubits")
    matrix = np.diag(diag).tolist()
    circ = QCircuit()
    circ << QOracle(qubits[:n], matrix)
    return circ

machine.finalize()
