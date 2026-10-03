# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

qvm = CPUQVM()
qvm.init()

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qubits = qvm.qAlloc_many(n)
    gate = QGate(np.diag(diag), qubits)
    circuit = QCircuit()
    circuit << gate
    return circuit

qvm.finalize()
