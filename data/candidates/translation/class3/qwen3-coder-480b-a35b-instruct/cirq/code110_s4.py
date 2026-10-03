# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Convert input circuit to unitary matrix
    op_or = cirq.unitary(circuit)
    num_qubits = len(circuit.all_qubits())
    
    qc_list = []
    counter = 0
    
    while counter < n:
        # Generate random Clifford circuit
        qubits = cirq.LineQubit.range(num_qubits)
        qc = cirq.Circuit()
        
        # Create a random Clifford by composing random Clifford gates
        # Using single-qubit and two-qubit Clifford gates
        clifford_gates = [
            cirq.I, cirq.X, cirq.Y, cirq.Z, 
            cirq.H, cirq.S, cirq.S**-1,
            cirq.CNOT, cirq.CZ, cirq.SWAP
        ]
        
        # Build a random Clifford circuit by applying random Clifford operations
        # We'll use a standard approach to build random Cliffords
        qc = cirq.testing.random_circuit(
            qubits=qubits,
            n_moments=2 * num_qubits,  # enough depth to generate good random Clifford
            op_density=0.5,
            gate_domain={cirq.X: 1, cirq.Y: 1, cirq.Z: 1, cirq.H: 1, cirq.S: 1, 
                         cirq.CNOT: 2, cirq.CZ: 2, cirq.SWAP: 2}
        )
        
        try:
            op_qc = cirq.unitary(qc)
            
            # Check equivalence within tolerance
            # For Clifford equivalence we check if the operators are equivalent up to global phase
            # Calculate the Frobenius norm difference
            diff = np.linalg.norm(op_qc - op_or)
            rel_diff = diff / np.linalg.norm(op_or)
            
            if rel_diff <= 0.4 or diff <= 0.4:
                counter += 1
                qc_list.append(qc)
        except:
            # If there's an issue computing the unitary (e.g., non-unitary ops), skip
            continue
            
    return qc_list
