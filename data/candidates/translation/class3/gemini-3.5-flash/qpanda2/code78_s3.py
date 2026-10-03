# EVAL_META: task_id=78, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

# Initialize global QVM
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(24)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = global_qubits[:num_qubits]
    for i in range(num_qubits):
        for j in range(i):
            angle = -np.pi / (2 ** (i - j))
            circuit << U1(qubits[i], angle).control([qubits[j]])
        circuit << H(qubits[i])
    return circuit

# Manual Cleanup
machine.finalize()
