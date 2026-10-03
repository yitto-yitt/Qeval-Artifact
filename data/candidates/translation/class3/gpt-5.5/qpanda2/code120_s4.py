# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)
atexit.register(machine.finalize)

def create_diagonal_circuit(diag):
    dim = len(diag)
    if dim == 0 or (dim & (dim - 1)) != 0:
        raise ValueError("The length of diag must be a positive power of 2.")
    num_qubits = int(math.log2(dim))
    if num_qubits > len(qubits):
        raise ValueError("Not enough globally allocated qubits.")

    prog = QProg()
    if num_qubits == 0:
        return prog

    matrix = [[0j for _ in range(dim)] for _ in range(dim)]
    for i, value in enumerate(diag):
        matrix[i][i] = complex(value)

    prog.insert(matrix_decompose(qubits[:num_qubits], matrix))
    return prog
