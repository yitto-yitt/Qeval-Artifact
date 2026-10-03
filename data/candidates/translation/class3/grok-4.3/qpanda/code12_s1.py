# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def get_unitary():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    mat = get_unitary_matrix(qvm, prog, qubits)
    qvm.finalize()
    return mat
