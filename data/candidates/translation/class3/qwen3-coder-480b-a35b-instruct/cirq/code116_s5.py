# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    qubits = cirq.LineQubit.range(n_qubits)
    
    # Convert pauli_string to cirq pauli terms
    pauli_terms = []
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            pauli_terms.append(cirq.X(qubits[i]))
        elif pauli_char == 'Y':
            pauli_terms.append(cirq.Y(qubits[i]))
        elif pauli_char == 'Z':
            pauli_terms.append(cirq.Z(qubits[i]))
        # For 'I', we don't add anything since identity doesn't contribute to the Hamiltonian
    
    if not pauli_terms:
        # If all identities, return empty circuit
        return cirq.Circuit()
    
    # Build the Hamiltonian as a sum of Pauli terms
    hamiltonian = cirq.PauliString()
    for term in pauli_terms:
        hamiltonian *= term
    
    # Create the evolution circuit by exponentiating the Hamiltonian
    # The evolution operator is exp(-i * time * H)
    circuit = cirq.Circuit()
    
    # If the hamiltonian is non-trivial, create the evolution
    if len(hamiltonian) > 0:
        # Calculate the eigenvalues and diagonalize
        # For a tensor product of Paulis, we can directly construct the evolution
        
        # Count non-identity terms to determine the effective evolution
        non_identity_count = sum(1 for p in pauli_string if p != 'I')
        
        if non_identity_count == 0:
            return cirq.Circuit()
        
        # For a single Pauli term, the evolution is straightforward
        # We build the circuit based on the specific Pauli operators
        circuit.append(cirq.pauli_string_expectation(
            cirq.PauliString({q: p for q, p in zip(qubits, [getattr(cirq, p) for p in pauli_string if p != 'I']) if p != 'I'}), 
            time).to_op())
        
        # Actually, let's build it more systematically
        pauli_ops = []
        for i, pauli_char in enumerate(pauli_string):
            if pauli_char == 'X':
                pauli_ops.append(cirq.X(qubits[i]))
            elif pauli_char == 'Y':
                pauli_ops.append(cirq.Y(qubits[i]))
            elif pauli_char == 'Z':
                pauli_ops.append(cirq.Z(qubits[i]))
        
        if pauli_ops:
            # Combine all Pauli operations into a PauliString
            combined_pauli = cirq.PauliString([op for op in pauli_ops])
            # Apply the exponential of the Pauli string
            circuit = cirq.Circuit(cirq.PauliStringPhasor(combined_pauli, exponent=-time))
        else:
            circuit = cirq.Circuit()
    
    else:
        circuit = cirq.Circuit()
    
    # More direct approach - build the evolution gate properly
    pauli_ops = []
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            pauli_ops.append(cirq.X(qubits[i]))
        elif pauli_char == 'Y':
            pauli_ops.append(cirq.Y(qubits[i]))
        elif pauli_char == 'Z':
            pauli_ops.append(cirq.Z(qubits[i]))
        # Identity ('I') is ignored
    
    if not pauli_ops:
        return cirq.Circuit()
    
    # Create a PauliString from the operators
    pauli_string_obj = cirq.PauliString(pauli_ops)
    
    # Create the evolution circuit using PauliStringPhasor which implements exp(-i*t*H)
    circuit = cirq.Circuit(cirq.PauliStringPhasor(pauli_string_obj, exponent=time/np.pi * np.pi))  # Correcting for the internal representation
    
    # Actually, the PauliStringPhasor applies exp(-i * π/2 * exponent * P) where P is the Pauli string
    # So to get exp(-i * t * P), we need to set exponent = t / (π/2) * (π/2) = t
    circuit = cirq.Circuit(cirq.PauliStringPhasor(pauli_string_obj, exponent=time))
    
    return circuit
