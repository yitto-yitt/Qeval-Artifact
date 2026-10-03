# EVAL_META: task_id=78, framework=qpanda, class=3
import pyqpanda3.core as pq

def qft_no_swaps(num_qubits):
    prog = pq.QProg()
    qubits = pq.qAlloc(num_qubits)
    
    # Implement inverse QFT without swaps
    for i in range(num_qubits):
        # Apply inverse Hadamard to the last qubit (reversed order)
        prog << pq.H(qubits[num_qubits - 1 - i])
        
        # Apply controlled phase gates in reverse order
        for j in range(i):
            # Apply controlled rotation with angle pi / 2^(i-j)
            angle = pq.PI / (2 ** (i - j))
            prog << pq.CU(qubits[num_qubits - 1 - j], qubits[num_qubits - 1 - i], 0, 0, -angle, 0)
    
    return prog, qubits
