# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, QVec, H, CP, SWAP
from numpy import pi

def QFT(n):
    if n == 0:
        return QProg()
    q = QVec(n)
    circ = QCircuit()
    
    def swap_registers(circ, n):
        for i in range(n // 2):
            circ << SWAP(q[i], q[n - i - 1])
        return circ

    def qft_rotations(circ, n):
        if n == 0:
            return circ
        n -= 1
        circ << H(q[n])
        for i in range(n):
            circ << CP(pi / 2**(n - i), q[i], q[n])
        qft_rotations(circ, n)
        
    qft_rotations(circ, n)
    swap_registers(circ, n)
    
    prog = QProg()
    prog << circ
    return prog
