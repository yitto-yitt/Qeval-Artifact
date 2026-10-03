# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qubits = machine.qAlloc_many(n)
    matrix = np.diag(np.asarray(diag, dtype=complex)).tolist()
    gate = QOracle(matrix)
    circuit = QCircuit()
    circuit << gate(*qubits)
    return circuit

machine.finalize()
