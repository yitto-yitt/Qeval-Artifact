# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)


def qft_no_swaps(num_qubits):
    prog = QProg()
    circ = QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))
            circ << CR(qubits[j], qubits[k], angle)
        circ << H(qubits[j])
    prog << circ
    return prog


if __name__ == "__main__":
    p = qft_no_swaps(3)
    print(p)
    machine.finalize()
