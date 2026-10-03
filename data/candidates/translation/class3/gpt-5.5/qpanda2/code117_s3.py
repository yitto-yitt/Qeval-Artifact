# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    data = unitary.data if hasattr(unitary, "data") else unitary
    matrix = np.asarray(data, dtype=np.complex128).reshape((4, 4))
    try:
        return matrix_decompose(_qubits, matrix)
    except Exception:
        return matrix_decompose(_qubits, matrix.reshape(-1).tolist())

atexit.register(lambda: machine.finalize())
