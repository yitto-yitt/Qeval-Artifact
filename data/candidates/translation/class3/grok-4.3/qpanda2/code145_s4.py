# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(20)
def qft_inverse(n):
    circuit = QCircuit()
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            circuit.insert(CR(qubits[j], qubits[i], -math.pi / 2**(j-i)))
        circuit.insert(H(qubits[i]))
    return circuit
machine.finalize()
