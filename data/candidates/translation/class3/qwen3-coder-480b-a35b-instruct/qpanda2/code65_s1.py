# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from math import pi

machine = pq.CPUQVM()
machine.init_qvm()

def QFT(n):
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    
    def swap_registers(prog, qubits, n):
        for qubit in range(n//2):
            prog << pq.SWAP(qubits[qubit], qubits[n-qubit-1])
        return prog
    
    def qft_rotations(prog, qubits, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return prog
        n -= 1
        prog << pq.H(qubits[n])
        for qubit in range(n):
            angle = pi / (2**(n-qubit))
            prog << pq.CR(qubits[qubit], qubits[n], angle)
        qft_rotations(prog, qubits, n)
    
    qft_rotations(prog, qubits, n)
    swap_registers(prog, qubits, len(qubits))
    
    # Return the program which represents the QFT circuit
    return prog

machine.finalize()
