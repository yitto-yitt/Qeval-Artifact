# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

_prog = pq.QProg()
_prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
_unitary = np.asarray(pq.get_unitary(_prog), dtype=complex)
if _unitary.shape != (4, 4):
    _unitary = _unitary.reshape((4, 4))


def get_unitary():
    return _unitary.copy()


machine.finalize()
