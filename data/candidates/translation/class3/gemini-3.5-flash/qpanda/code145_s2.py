# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, U1, SWAP
import math

def qft_inverse(n):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    prog = QCircuit()
    
    # Keep machine alive by attaching it to the circuit
    prog.machine = machine
    
    # 1. Swaps
    for i in range(n // 2):
        prog << SWAP(qubits[i], qubits[n - 1 - i])
        
    # 2. Inverse QFT core
    for i in range(n):
        for j in range(i):
            angle = -2.0 * math.pi / (2 ** (i - j + 1))
            prog << U1(qubits[i], angle).control([qubits[j]])
        prog << H(qubits[i])
        
    return prog
