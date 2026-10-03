# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(29)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = [global_qubits[i] for i in range(num_qubits)]
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit

machine.finalize()
