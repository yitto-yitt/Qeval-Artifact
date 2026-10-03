# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = [cirq.LineQubit(i) for i in range(n_qubits)]
    circuit = cirq.Circuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to Cirq Pauli terms
        pauli_ops = []
        for i, pauli_char in enumerate(pauli_string):
            if pauli_char == 'X':
                pauli_ops.append(cirq.X(qubits[i]))
            elif pauli_char == 'Y':
                pauli_ops.append(cirq.Y(qubits[i]))
            elif pauli_char == 'Z':
                pauli_ops.append(cirq.Z(qubits[i]))
        
        # Combine into a single PauliString
        pauli_term = cirq.PauliString(pauli_ops)
        
        # Apply Trotterized evolution - for Lie-Trotter we use first-order approximation
        # Each repetition applies the evolution operator
        for _ in range(reps):
            # For each term in the Hamiltonian (in this case just one term per iteration)
            circuit.append(cirq.ApproximatelyEigenDecomposedPauliString(
                pauli_string=pauli_term,
                exponent=-time * 2 / np.pi,  # Adjust for Cirq's convention
                phases_enabled=True
            ))
    
    return circuit
