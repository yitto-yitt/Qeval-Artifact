# EVAL_META: task_id=145, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
import math

def qft_inverse(n):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = [machine.qAlloc() for _ in range(n)]
    
    prog = QProg()
    
    # Apply inverse QFT: reverse the order of operations from normal QFT
    for i in range(n-1, -1, -1):
        # Hadamard gate on current qubit
        prog << pq.H(qubits[i])
        
        # Apply controlled rotations in reverse order
        for j in range(i):
            angle = -math.pi / (2 ** (i - j))
            prog << pq.CR(qubits[j], qubits[i], angle)
    
    # Reverse the qubit order to complete the inverse QFT
    for i in range(n // 2):
        prog << pq.SWAP(qubits[i], qubits[n - 1 - i])
    
    return prog, qubits, machine
