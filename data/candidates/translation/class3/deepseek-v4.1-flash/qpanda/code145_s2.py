# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, Qubit, H, CPHASE, SWAP

def qft_inverse(n):
    circuit = QCircuit()
    qubits = [Qubit() for _ in range(n)]
    
    # Swap qubits at the beginning (inverse of swaps at end of forward QFT)
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])
    
    # Inverse of forward QFT gates
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            control = n - 1 - j
            target = n - 1 - i
            angle = -math.pi / (2 ** (j - i))
            circuit << CPHASE(qubits[control], qubits[target], angle)
        circuit << H(qubits[n - 1 - i])
    
    return circuit
