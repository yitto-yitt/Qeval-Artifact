# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def get_unitary():
    U = np.zeros((4, 4), dtype=complex)
    for j in range(4):
        prog = QProg()
        if j & 1:
            prog << X(qubits[0])
        if (j >> 1) & 1:
            prog << X(qubits[1])
        prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        machine.run(prog)
        state = machine.get_qstate()
        for i in range(4):
            U[i][j] = state[i]
    return U

if __name__ == "__main__":
    machine.finalize()
