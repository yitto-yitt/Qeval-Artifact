# EVAL_META: task_id=4, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 0, 0, 0],
         [0, 1, 0, 0]],
        dtype=np.complex128
    )
    flat_matrix = [complex(x) for x in matrix.reshape(-1)]

    for mat in (flat_matrix, matrix, matrix.tolist()):
        try:
            circuit = QProg()
            circuit << QOracle(qubits, mat)
            return circuit
        except Exception:
            pass

    for args in ((qubits, matrix), (qubits, flat_matrix), (matrix, qubits), (flat_matrix, qubits)):
        try:
            decomposed = matrix_decompose(*args)
            circuit = QProg()
            circuit << decomposed
            return circuit
        except Exception:
            pass

    circuit = QProg()
    circuit << CNOT(qubits[1], qubits[0]) << X(qubits[1])
    return circuit

atexit.register(lambda: machine.finalize())
