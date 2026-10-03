# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq


def get_unitary():
    pq.init_qvm()
    qubits = pq.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    matrix = pq.get_matrix(prog, qubits)
    pq.finalize()
    return matrix
