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
        
        # If there are non-identity terms, create the evolution
        if pauli_ops:
            # For Lie-Trotter we treat each term separately
            for _ in range(reps):
                for pauli_op in pauli_ops:
                    # Apply the evolution gate for the given time divided by reps
                    circuit.append(pauli_op**(time / reps))
    
    return circuit
