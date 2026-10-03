# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda import *
from numpy import pi

def QFT(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n)
    
    prog = QProg()
    
    def swap_registers(prog, qubits, n):
        for i in range(n // 2):
            prog.insert(SWAP(qubits[i], qubits[n-i-1]))
        return prog
    
    def qft_rotations(prog, qubits, n):
        if n == 0:
            return prog
        n -= 1
        prog.insert(H(qubits[n]))
        for i in range(n):
            prog.insert(CR(qubits[i], qubits[n], pi / 2**(n-i)))
        qft_rotations(prog, qubits, n)
    
    qft_rotations(prog, qubits, n)
    swap_registers(prog, qubits, n)
    
    return prog
