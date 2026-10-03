# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(2)

_finalized = False

def _finalize_machine():
    global _finalized
    if not _finalized:
        try:
            machine.finalize()
        finally:
            _finalized = True

atexit.register(_finalize_machine)

def decompose_unitary(unitary):
    data = unitary.data if hasattr(unitary, "data") else unitary
    mat = np.asarray(data, dtype=complex).reshape((4, 4))
    try:
        return pq.matrix_decompose(_qubits, mat)
    except TypeError:
        return pq.matrix_decompose(_qubits, mat.tolist())
