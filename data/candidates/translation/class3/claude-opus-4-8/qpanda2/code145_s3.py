# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)


def qft_inverse(n):
    circ = QCircuit()

    # Reverse swaps first (inverse of QFT's final swaps)
    for i in range(n // 2):
        circ << SWAP(qubits[i], qubits[n - 1 - i])

    # Inverse of the QFT rotations, applied in reverse order
    for j in reversed(range(n)):
        for k in reversed(range(j)):
            angle = -np.pi / (2 ** (j - k))
            circ << CR(qubits[k], qubits[j], angle)
        circ << H(qubits[j])

    return circ


if __name__ == "__main__":
    n = 3
    circ = qft_inverse(n)
    prog = QProg()
    prog << circ
    print(prog)
    machine.finalize()
