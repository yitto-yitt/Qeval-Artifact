# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def get_unitary():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])

    unitary = qvm.get_unitary(prog, qubits)
    qvm.finalize()
    return np.array(unitary)
