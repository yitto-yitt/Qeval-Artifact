# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math
import atexit

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)

def qft_inverse(n):
    if n < 0 or n > len(_qubits):
        raise ValueError("invalid number of qubits")

    qubits = _qubits[:n]
    circuit = QCircuit()

    for i in range(n // 2):
        circuit.insert(SWAP(qubits[i], qubits[n - i - 1]))

    for j in range(n):
        for k in range(j):
            circuit.insert(CR(qubits[k], qubits[j], -math.pi / (2 ** (j - k))))
        circuit.insert(H(qubits[j]))

    return circuit

atexit.register(machine.finalize)
