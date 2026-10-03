# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def qft_no_swaps(num_qubits):
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    
    # Implement inverse QFT without swaps
    for i in range(num_qubits):
        # Apply inverse H gate
        prog << pq.H(qubits[num_qubits - 1 - i])
        
        # Apply inverse controlled rotations
        for j in range(i):
            angle = -1 * (2 * 3.141592653589793) / (2 ** (i - j + 1))
            prog << pq.CR(qubits[num_qubits - 1 - j], qubits[num_qubits - 1 - i], angle)
    
    return prog, qubits

def finalize():
    machine.finalize()
