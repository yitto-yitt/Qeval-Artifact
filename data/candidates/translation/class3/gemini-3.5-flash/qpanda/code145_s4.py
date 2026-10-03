# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def qft_inverse(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    
    circuit = QCircuit()
    
    # Swaps
    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])
        
    # Inverse QFT rotations and H gates
    for i in range(n):
        for j in range(i):
            theta = -2 * math.pi / (2 ** (i - j + 1))
            circuit << CR(q[j], q[i], theta)
        circuit << H(q[i])
        
    return circuit
