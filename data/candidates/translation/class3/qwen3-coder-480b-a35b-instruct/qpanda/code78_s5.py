# EVAL_META: task_id=78, framework=qpanda, class=3
import pyqpanda3.core as pq

def qft_no_swaps(num_qubits):
    prog = pq.QProg()
    q = pq.qAlloc(num_qubits)
    
    # Apply inverse QFT without swaps - reverse the order of operations compared to normal QFT
    for i in range(num_qubits):
        # Apply Hadamard gate
        prog << pq.H(q[num_qubits - 1 - i])
        
        # Apply controlled phase rotations
        for j in range(i + 1, num_qubits):
            angle = -2 * pq.PI / (2 ** (j - i + 1))
            prog << pq.CU(q[j], q[num_qubits - 1 - i], 0, 0, angle)
    
    return prog, q
