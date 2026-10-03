# EVAL_META: task_id=4, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QCircuit, U4

_QVM = None

def create_unitary_from_matrix():
    global _QVM
    if _QVM is None:
        _QVM = CPUQVM()
        _QVM.init_qvm()

    qubits = _QVM.qAlloc_many(2)

    matrix = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ], dtype=complex)

    circuit = QCircuit()
    circuit << U4(matrix, qubits[0], qubits[1])
    return circuit
