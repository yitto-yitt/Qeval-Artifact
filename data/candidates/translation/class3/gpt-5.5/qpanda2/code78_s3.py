# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

_MAX_QUBITS = 20

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(_MAX_QUBITS)
atexit.register(machine.finalize)

def qft_no_swaps(num_qubits):
    if num_qubits < 0:
        raise ValueError("num_qubits must be non-negative")
    if num_qubits > _MAX_QUBITS:
        raise ValueError("num_qubits exceeds globally allocated qubits")

    circuit = QCircuit()

    for j in range(num_qubits):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circuit.insert(CR(q[k], q[j], angle))
        circuit.insert(H(q[j]))

    return circuit
