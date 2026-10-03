# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import math
import atexit

machine = CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(256)
atexit.register(machine.finalize)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = _global_qubits[:num_qubits]

    for j in range(num_qubits):
        circuit.insert(H(qubits[j]))
        for k in range(j + 1, num_qubits):
            angle = -math.pi / (2 ** (k - j))
            circuit.insert(CR(qubits[k], qubits[j], angle))

    return circuit
