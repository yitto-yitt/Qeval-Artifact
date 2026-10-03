# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(20)
atexit.register(machine.finalize)

def create_diagonal_circuit(diag):
    dim = len(diag)
    num_qubits = int(math.log2(dim)) if dim > 0 else 0
    if dim != (1 << num_qubits):
        raise ValueError("Diagonal length must be a power of 2.")
    if num_qubits > len(_qubits):
        raise ValueError("Not enough globally allocated qubits.")

    prog = QProg()
    if num_qubits == 0:
        return prog

    matrix = [[0j for _ in range(dim)] for _ in range(dim)]
    for i, value in enumerate(diag):
        matrix[i][i] = complex(value)

    qvec = [_qubits[i] for i in range(num_qubits)]
    prog << matrix_decompose(qvec, matrix)
    return prog
