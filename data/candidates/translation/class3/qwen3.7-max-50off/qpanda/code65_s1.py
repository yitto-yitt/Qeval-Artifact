# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
from numpy import pi

def QFT(n):
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qalloc_many(n)
    circ = QCircuit()
    
    def qft_rotations(circ, n):
        if n == 0:
            return
        n -= 1
        circ << H(q[n])
        for qubit in range(n):
            circ << CP(pi / 2**(n - qubit), q[qubit], q[n])
        qft_rotations(circ, n)
        
    qft_rotations(circ, n)
    
    for i in range(n // 2):
        circ << SWAP(q[i], q[n - i - 1])
        
    prog = QProg()
    prog << circ
    return prog
