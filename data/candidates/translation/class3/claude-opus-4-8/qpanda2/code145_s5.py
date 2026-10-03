# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def qft_inverse(n):
    circ = QCircuit()
    for i in range(n // 2):
        circ << SWAP(qubits[i], qubits[n - 1 - i])
    for j in range(n):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circ << CR(qubits[k], qubits[j], angle)
        circ << H(qubits[j])
    return circ

if __name__ == "__main__":
    c = qft_inverse(3)
    print(c)
    machine.finalize()
