# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    # Determine the number of qubits from the first Pauli string
    num_qubits = len(pauli_strings[0])
    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    
    # Create the circuit
    circuit = cirq.Circuit()
    
    # Process each Pauli string and its corresponding time
    for pauli_string, time in zip(pauli_strings, times):
        # Create the Hamiltonian as a sum of Pauli terms
        pauli_ops = []
        for i, char in enumerate(pauli_string):
            if char == 'X':
                pauli_ops.append(cirq.X(qubits[i]))
            elif char == 'Y':
                pauli_ops.append(cirq.Y(qubits[i]))
            elif char == 'Z':
                pauli_ops.append(cirq.Z(qubits[i]))
        
        # For a single Pauli string, we can create a PauliString directly
        pauli_string_op = cirq.PauliString(dict(zip(qubits, pauli_string)))
        hamiltonian = pauli_string_op
        
        # Apply the Lie-Trotter formula by repeating the evolution gate
        # Since we're implementing LieTrotter of order 1 (basic product formula)
        # we simply repeat the individual evolutions
        for _ in range(reps):
            # Evolve under the Hamiltonian for time 'time'
            # In Cirq, we use cirq.PauliStringPhasor for exponentiating Pauli strings
            # which implements exp(-i * theta * P) where P is the Pauli string
            # We need to adjust the sign and factor of 2 to match conventions
            theta = -time / np.pi  # Convert to angle in Cirq's convention
            evolution_gate = cirq.PauliStringPhasor(hamiltonian, exponent_scalar=theta)
            circuit.append(evolution_gate)
            
    return circuit
