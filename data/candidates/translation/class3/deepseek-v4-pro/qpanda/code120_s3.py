# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QCircuit, QOracle

_qvm = CPUQVM()
_qvm.init()

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qubits = _qvm.qAlloc_many(n)
    circuit = QCircuit()
    circuit << QOracle(qubits, np.diag(diag))
    return circuit
