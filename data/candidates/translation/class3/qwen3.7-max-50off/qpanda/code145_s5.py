# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, QVec, H, SWAP, CP

def qft_inverse(n):
    q = QVec(n)
    circ = QCircuit()
    
    for i in range(n // 2):
        circ << SWAP(q[i], q[n - i - 1])
        
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            circ << CP(q[j], q[k], -math.pi / (2 ** (k - j)))
        circ << H(q[j])
        
    return circ
