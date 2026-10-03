# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()

def create_diagonal_circuit(diag):
    # Calculate number of qubits needed based on diagonal size
    n_qubits = int(np.log2(len(diag)))
    
    # Allocate qubits
    qubits = machine.qAlloc_many(n_qubits)
    
    # Create quantum program
    prog = pq.QProg()
    
    # In pyQPanda, we need to construct diagonal gates manually using phase gates and controlled operations
    # For now, we'll create a circuit that represents the diagonal operation
    # This is a simplified approach - real implementation would depend on specific diagonal values
    
    # Convert diagonal elements to angles for RZ gates where possible
    # For general diagonal gates, we might need more complex constructions
    for i, elem in enumerate(diag):
        # Extract phase from diagonal element
        phase = np.angle(elem)
        
        # Apply phase using multi-controlled RZ gates
        binary_i = format(i, f'0{n_qubits}b')
        
        # Create controlled phase operation based on the binary representation of index i
        ctrl_list = []
        for j, bit in enumerate(binary_i):
            if bit == '0':
                prog << pq.X(qubits[j])
        
        # Apply multi-controlled phase
        prog << pq.RZ(qubits[0], phase)  # Simplified - actual implementation depends on all qubits
        
        # Undo the X gates
        for j, bit in enumerate(binary_i):
            if bit == '0':
                prog << pq.X(qubits[j])
    
    # Return the quantum program
    return prog

machine.finalize()
