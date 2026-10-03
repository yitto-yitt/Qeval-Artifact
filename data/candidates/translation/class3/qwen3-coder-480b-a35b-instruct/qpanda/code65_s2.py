# EVAL_META: task_id=65, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def QFT(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    
    def swap_registers(prog, qubits, n):
        for qubit in range(n//2):
            prog << SWAP(qubits[qubit], qubits[n-qubit-1])
        return prog
    
    def qft_rotations(prog, qubits, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return prog
        n -= 1
        prog << H(qubits[n])
        for qubit in range(n):
            angle = math.pi / (2**(n-qubit))
            prog << CR(qubits[qubit], qubits[n], angle)
        qft_rotations(prog, qubits, n)
    
    qft_rotations(prog, qubits, n)
    swap_registers(prog, qubits, n)
    
    return prog
