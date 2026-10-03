# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit, H, CP, SWAP
import numpy as np

def QFT(n):
    qm = QMachine()
    q = qm.allocate_qubits(n)
    circ = QCircuit()
    
    def swap_registers(c, n):
        for i in range(n // 2):
            c << SWAP(q[i], q[n - i - 1])
            
    def qft_rotations(c, n):
        if n == 0:
            return
        n -= 1
        c << H(q[n])
        for i in range(n):
            c << CP(np.pi / 2**(n - i), q[i], q[n])
        qft_rotations(c, n)
        
    qft_rotations(circ, n)
    swap_registers(circ, n)
    
    return circ
