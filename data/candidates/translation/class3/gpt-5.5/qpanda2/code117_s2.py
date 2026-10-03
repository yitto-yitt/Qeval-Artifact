# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    if hasattr(unitary, "data"):
        mat = np.asarray(unitary.data, dtype=np.complex128)
    else:
        mat = np.asarray(unitary, dtype=np.complex128)

    if mat.shape != (4, 4):
        mat = mat.reshape((4, 4))

    candidates = [
        mat.reshape(-1).tolist(),
        mat.tolist(),
        mat,
    ]

    last_error = None
    for candidate in candidates:
        for args in ((_qubits, candidate), (candidate, _qubits)):
            try:
                return matrix_decompose(*args)
            except Exception as exc:
                last_error = exc

    raise last_error

atexit.register(machine.finalize)
