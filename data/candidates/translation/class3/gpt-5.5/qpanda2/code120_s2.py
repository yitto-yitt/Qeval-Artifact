# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)

def create_diagonal_circuit(diag):
    dim = len(diag)
    if dim == 0 or (dim & (dim - 1)) != 0:
        raise ValueError("Length of diagonal must be a positive power of 2.")
    num_qubits = int(math.log2(dim))
    if num_qubits > len(qubits):
        raise ValueError("Not enough globally allocated qubits.")
    prog = pq.QProg()
    if num_qubits == 0:
        return prog
    qvec = [qubits[i] for i in range(num_qubits)]
    matrix = np.diag(np.asarray(diag, dtype=complex)).tolist()
    prog.insert(pq.matrix_decompose(qvec, matrix))
    return prog

atexit.register(machine.finalize)
