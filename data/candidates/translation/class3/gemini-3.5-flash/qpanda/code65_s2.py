# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def QFT(n):
    global _global_machine
    if '_global_machine' not in globals():
        _global_machine = CPUQVM()
        _global_machine.init_qvm()
    
    qubits = _global_machine.qAlloc_many(n)
    prog = QProg()
    
    def qft_rotations(n):
        if n == 0:
            return
        n -= 1
        prog << H(qubits[n])
        for qubit in range(n):
            prog << CR(qubits[qubit], qubits[n], np.pi / (2**(n - qubit)))
        qft_rotations(n)
        
    qft_rotations(n)
    
    for qubit in range(n // 2):
        prog << SWAP(qubits[qubit], qubits[n - qubit - 1])
        
    return prog
