# EVAL_META: task_id=41, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    prog = QProg()
    prog.insert(X(qubits[0]))
    prog.insert(I(qubits[1]))
    prog.insert(Y(qubits[2]))
    mat = np.array(get_matrix(prog), dtype=complex)
    if mat.ndim == 1:
        mat = mat.reshape((8, 8))
    return mat


atexit.register(machine.finalize)
