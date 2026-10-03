# EVAL_META: task_id=78, framework=qpanda, class=3
import pyqpanda3.core as pq

def qft_no_swaps(num_qubits):
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(num_qubits)
    
    # Inverse QFT without swaps - apply inverse QFT operations
    for i in range(num_qubits):
        # Apply Hadamard gate
        qvm.h(q[num_qubits - 1 - i])
        
        # Apply controlled phase shift gates
        for j in range(i):
            # Calculate the angle for the controlled phase shift
            angle = -2 * 3.141592653589793 / (2 ** (i - j + 1))
            qvm.cu1(q[num_qubits - 1 - j], q[num_qubits - 1 - i], angle)
    
    return qvm.get_circuit()
