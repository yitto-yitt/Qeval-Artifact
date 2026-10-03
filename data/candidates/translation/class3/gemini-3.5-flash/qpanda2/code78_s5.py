# EVAL_META: task_id=78, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qlist = machine.qAlloc_many(100)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = qlist[:num_qubits]
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            circuit << CU1(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit

machine.finalize()
