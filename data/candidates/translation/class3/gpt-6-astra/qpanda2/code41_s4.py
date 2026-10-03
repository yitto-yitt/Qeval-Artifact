# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    try:
        program = pq.QProg()
        program << pq.X(qubits[0]) << pq.I(qubits[1]) << pq.Y(qubits[2])
        return np.asarray(pq.get_matrix(program, False), dtype=complex).reshape(8, 8)
    finally:
        machine.finalize()
