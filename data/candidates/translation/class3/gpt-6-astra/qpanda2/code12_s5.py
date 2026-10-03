# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    try:
        prog = pq.QProg()
        prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
        return np.asarray(pq.get_matrix(prog), dtype=complex).reshape(4, 4)
    finally:
        machine.finalize()
