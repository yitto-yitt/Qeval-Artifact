# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *


machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(2)


def get_unitary():
    dim = 4
    U = np.zeros((dim, dim), dtype=complex)
    for basis in range(dim):
        prog = QProg()
        for i in range(2):
            if (basis >> i) & 1:
                prog << X(qubits[i])
        prog << H(qubits[0])
        prog << CNOT(qubits[0], qubits[1])
        machine.run(prog)
        state = machine.get_qstate()
        for j in range(dim):
            U[j, basis] = state[j]
    machine.finalize()
    return U
