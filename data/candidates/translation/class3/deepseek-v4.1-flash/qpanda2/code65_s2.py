# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def QFT(n):
    prog = QProg()
    for i in range(n-1, -1, -1):
        prog << H(qubits[i])
        for j in range(i):
            angle = pi / (2 ** (i - j))
            prog << CR(qubits[j], qubits[i], angle)
    for i in range(n//2):
        prog << SWAP(qubits[i], qubits[n-i-1])
    return prog

machine.finalize()
