# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)

def qft_inverse(n):
    circ = QCircuit()
    # inverse QFT: reverse of QFT
    # QFT: for j in range(n): H(j); controlled phase; then swaps
    # inverse = dagger of QFT
    qft = QCircuit()
    for j in range(n):
        qft << H(qubits[j])
        for k in range(j + 1, n):
            angle = np.pi / (2 ** (k - j))
            qft << CR(qubits[k], qubits[j], angle)
    for i in range(n // 2):
        qft << SWAP(qubits[i], qubits[n - 1 - i])
    circ = qft.dagger()
    return circ

if __name__ == "__main__":
    c = qft_inverse(3)
    prog = QProg()
    prog << c
    print(prog)
    machine.finalize()
