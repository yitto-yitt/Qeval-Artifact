# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def qft_inverse(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    circuit = QProg()
    for i in range(n):
        circuit << H(qubits[i])
        for j in range(i + 1, n):
            circuit << CR(qubits[j], qubits[i], -math.pi / 2 ** (j - i))
    return circuit
