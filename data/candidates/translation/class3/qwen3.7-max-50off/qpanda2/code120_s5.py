# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(15)

def create_diagonal_circuit(diag):
    n = int(round(np.log2(len(diag))))
    prog = pq.QProg()
    mat = np.diag(diag).tolist()
    prog << pq.Unitary(qubits[:n], mat)
    return prog

machine.finalize()
