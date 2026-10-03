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
    
    # In pyQPanda, we need to construct diagonal gates manually using phase gates and multiplexors
    # For now, we'll use a general approach creating the unitary matrix from diagonal elements
    
    # Convert diagonal elements to a unitary matrix (diagonal matrix)
    dim = len(diag)
    unitary_matrix = np.diag(diag)
    
    # Apply diagonal gate by constructing the appropriate circuit
    # For a diagonal gate, we can decompose it into a sequence of controlled-phase gates
    for i in range(dim):
        # Extract phase for each computational basis state
        phase = np.angle(diag[i])
        
        # Create controlled-Z type operations to implement the phase
        # This is a simplified implementation - actual decomposition may vary
        if abs(phase) > 1e-6:  # Only add gate if phase is significant
            # For diagonal gates, we implement multi-controlled phase gates
            binary_i = bin(i)[2:].zfill(n_qubits)
            
            # Build the control mask
            controls = []
            for j, bit in enumerate(binary_i):
                if bit == '1':
                    controls.append(qubits[j])
                    
            # If all bits are 1 (for state |11...1>), apply a phase gate
            if all(bit == '1' for bit in binary_i):
                prog.insert(pq.RZ(qubits[0], phase))  # Simplified - actual implementation would be more complex
            else:
                # For other states, we'd need multi-controlled rotations
                # This is a simplified placeholder
                pass
                
    # A more accurate approach is to use pyqpanda's diagonal gate functionality if available
    # Since pyQPanda might not have a direct diagonal gate, we construct the equivalent circuit
    # Using U gates to implement phases for each basis state
    
    # Reset the program and use a more direct approach
    prog = pq.QProg()
    
    # For diagonal gates in pyQPanda, we'll build the circuit using rotation gates
    # that apply the required phase shifts
    
    # Create the full diagonal gate implementation
    # Since pyQPanda doesn't have a direct diagonal gate, we implement using multiplexed RZ gates
    
    # Create a new program to implement the diagonal operation
    prog = pq.QProg()
    
    # For each diagonal element, we need to conditionally apply the phase
    # based on the computational basis state
    for state_idx in range(len(diag)):
        # Get the binary representation of the state index
        binary_state = format(state_idx, f'0{n_qubits}b')
        
        # Create a controlled phase operation for this specific state
        # This requires ancilla-based implementation in practice
        
    # Actually, let's use pyqpanda's built-in diagonal functionality if available
    # Or implement using basic gates
    
    # The most straightforward way in pyQPanda is to use the diagonal matrix directly
    # if the interface supports it, otherwise decompose into basic gates
    prog = pq.QProg()
    
    # Add diagonal gate using pyqpanda's diagonal gate implementation
    prog.insert(pq.DiagU(qubits, diag))
    
    return (prog, qubits)

# Clean up at the end of execution
import atexit
atexit.register(lambda: machine.finalize())
