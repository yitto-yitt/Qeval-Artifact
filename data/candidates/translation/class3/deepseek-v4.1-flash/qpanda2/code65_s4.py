# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(20)

def QFT(n):
    circ = QCircuit()
    for i in range(n - 1, -1, -1):
        circ << H(qubits[i])
        for j in range(i):
            circ << CP(qubits[j], qubits[i], pi / (2 ** (i - j)))
    for i in range(n // 2):
        circ << SWAP(qubits[i], qubits[n - i - 1])
    return circ

if __name__ == "__main__":
    qvm.finalize()
