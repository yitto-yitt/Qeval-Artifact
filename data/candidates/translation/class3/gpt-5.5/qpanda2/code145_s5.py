# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math
import atexit

MAX_QUBITS = 20

machine = CPUQVM()
machine.init_qvm()
qv = machine.qAlloc_many(MAX_QUBITS)

def qft_inverse(n):
    if n < 0 or n > MAX_QUBITS:
        raise ValueError("n is out of the allocated qubit range")

    qubits = [qv[i] for i in range(n)]
    circuit = QCircuit()

    for i in range(n // 2):
        circuit.insert(SWAP(qubits[i], qubits[n - i - 1]))

    for j in range(n):
        for k in range(j):
            circuit.insert(CR(qubits[j], qubits[k], -math.pi / (2 ** (j - k))))
        circuit.insert(H(qubits[j]))

    return circuit

atexit.register(machine.finalize)
