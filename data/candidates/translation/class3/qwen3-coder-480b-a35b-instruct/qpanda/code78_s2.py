# EVAL_META: task_id=78, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
import math

def qft_no_swaps(num_qubits):
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    
    prog = QProg()
    
    # Apply inverse QFT without swaps - reverse order of operations compared to forward QFT
    for i in range(num_qubits):
        # Apply Hadamard gate
        prog << pq.H(qubits[num_qubits - 1 - i])
        
        # Apply controlled phase shift gates
        for j in range(i + 1, num_qubits):
            angle = -math.pi / (2 ** (j - i))
            prog << pq.CR(qubits[num_qubits - 1 - j], qubits[num_qubits - 1 - i], angle)
    
    qvm.finalize()
    return prog
