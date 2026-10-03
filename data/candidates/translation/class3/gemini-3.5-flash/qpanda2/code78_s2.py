# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
from pyqpanda import *

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(24)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = q[:num_qubits]
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -math.pi / (2 ** (j - i))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit

# Manual Cleanup
machine.finalize()
