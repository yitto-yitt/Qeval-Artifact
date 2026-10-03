# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
import math

machine = pq.CPUQVM()
machine.init_qvm()

def qft_inverse(n):
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    
    # Apply inverse QFT: reverse order of operations from regular QFT
    for i in range(n):
        # Apply Hadamard gate to the current qubit
        prog << pq.H(qubits[n - 1 - i])
        
        # Apply controlled phase gates in reverse order
        for j in range(i + 1, n):
            angle = -math.pi / (2 ** (j - i))
            prog << pq.CR(qubits[n - 1 - j], qubits[n - 1 - i], angle)
    
    # Reverse the order of qubits to complete the inverse QFT
    for i in range(n // 2):
        prog << pq.SWAP(qubits[i], qubits[n - 1 - i])
    
    return prog, qubits

# Clean up
machine.finalize()
