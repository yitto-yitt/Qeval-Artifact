# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    data = getattr(unitary, "data", unitary)
    if callable(data):
        data = data()
    matrix = np.asarray(data, dtype=np.complex128)
    return pq.matrix_decompose(_qubits, matrix)

atexit.register(machine.finalize)
