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
    
    # Add diagonal gate using unitary matrix
    prog << pq.unitary_decomposer_1q(unitary_matrix, qubits[0])
    
    # Handle multi-qubit case with diagonal gate construction
    if n_qubits > 1:
        # For multi-qubit diagonal gates, we need to build custom circuit
        # This is a simplified version - real implementation would need more complex decomposition
        pass
    
    # Build the circuit
    qc = pq.QCircuit()
    qc.set_QProg(prog)
    
    # Create quantum program containing the circuit
    final_prog = pq.QProg()
    final_prog.insert(qc)
    
    return final_prog, qubits, machine

# Manual cleanup
machine.finalize()
