# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math

# Global QVM
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(24)

def qft_inverse(n):
    circuit = QCircuit()
    if n <= 0:
        return circuit
    qubits = global_qubits[:n]
    
    # 1. Swap qubits
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])
        
    # 2. Controlled rotations and H gates
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            theta = -math.pi / (2 ** (j - i))
            circuit << U1(qubits[i], theta).control([qubits[j]])
        circuit << H(qubits[i])
        
    return circuit

machine.finalize()
