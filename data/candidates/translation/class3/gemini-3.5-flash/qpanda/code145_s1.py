# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def qft_inverse(n):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    
    circuit = QCircuit()
    
    # Swap qubits at the beginning of inverse QFT
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])
        
    for i in range(n):
        circuit << H(qubits[i])
        for j in range(i + 1, n):
            theta = -math.pi / (2 ** (j - i))
            circuit << CR(qubits[j], qubits[i], theta)
            
    return circuit
