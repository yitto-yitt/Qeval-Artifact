# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)

def QFT(n):
    qubits = q[:n]
    circ = QCircuit()
    
    def qft_rotations(circ, n):
        if n == 0:
            return circ
        n -= 1
        circ << H(qubits[n])
        for i in range(n):
            circ << CR(qubits[i], qubits[n], np.pi / (2**(n-i)))
        qft_rotations(circ, n)
        
    def swap_registers(circ, n):
        for i in range(n//2):
            circ << SWAP(qubits[i], qubits[n-i-1])
        return circ

    qft_rotations(circ, n)
    swap_registers(circ, n)
    
    prog = QProg()
    prog << circ
    return prog

machine.finalize()
