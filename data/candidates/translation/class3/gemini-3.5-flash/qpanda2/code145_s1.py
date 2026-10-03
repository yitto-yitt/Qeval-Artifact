# EVAL_META: task_id=145, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

# Initialize global QVM
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def qft_inverse(n):
    circuit = QCircuit()
    if n <= 0:
        return circuit
    
    q = [global_qubits[i] for i in range(n)]
    
    # Swap qubits
    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])
        
    # Apply H and CP gates
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            g = U1(q[i], angle)
            qvec = QVec()
            qvec.push_back(q[j])
            circuit << g.control(qvec)
        circuit << H(q[i])
        
    return circuit

machine.finalize()
