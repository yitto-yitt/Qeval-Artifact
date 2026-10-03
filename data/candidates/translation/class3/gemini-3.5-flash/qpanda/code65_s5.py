# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def QFT(n):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAllocMany(n)
    prog = QProg()
    
    def qft_rotations(prog, qubits, n):
        if n == 0:
            return
        n -= 1
        prog << H(qubits[n])
        for qubit in range(n):
            prog << CR(qubits[qubit], qubits[n], np.pi / (2 ** (n - qubit)))
        qft_rotations(prog, qubits, n)
        
    def swap_registers(prog, qubits, n):
        for qubit in range(n // 2):
            prog << SWAP(qubits[qubit], qubits[n - qubit - 1])
            
    qft_rotations(prog, qubits, n)
    swap_registers(prog, qubits, n)
    return prog
