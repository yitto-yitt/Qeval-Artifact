# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    program = pq.QProg()
    program << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    return np.asarray(pq.get_matrix(program, False), dtype=complex).reshape(4, 4)


atexit.register(lambda: machine.finalize())
