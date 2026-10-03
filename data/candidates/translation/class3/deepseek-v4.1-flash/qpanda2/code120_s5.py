# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = (len(diag) - 1).bit_length()
    q = qubits[:n][::-1]
    matrix = np.diag(np.array(diag, dtype=complex))
    oracle = QOracle(q, matrix)
    circuit = QCircuit()
    circuit << oracle
    return circuit

machine.finalize()
