# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
try:
    machine.set_configure(64, 64)
except Exception:
    pass
machine.init_qvm()
_qubits = machine.qAlloc_many(64)

def qft_inverse(n):
    circuit = QCircuit()
    qs = _qubits[:n]

    for i in range(n // 2):
        circuit.insert(SWAP(qs[i], qs[n - i - 1]))

    for j in range(n):
        for m in range(j):
            angle = -math.pi / (2 ** (j - m))
            circuit.insert(U1(qs[j], angle).control([qs[m]]))
        circuit.insert(H(qs[j]))

    return circuit

atexit.register(machine.finalize)
