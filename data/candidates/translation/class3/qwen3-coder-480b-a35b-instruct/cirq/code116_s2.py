# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    qubits = cirq.LineQubit.range(n_qubits)
    
    # Convert pauli_string to cirq pauli operations
    pauli_ops = []
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            pauli_ops.append(cirq.X(qubits[i]))
        elif pauli_char == 'Y':
            pauli_ops.append(cirq.Y(qubits[i]))
        elif pauli_char == 'Z':
            pauli_ops.append(cirq.Z(qubits[i]))
        # For 'I', we don't add anything since identity doesn't affect the evolution
    
    # Build the Hamiltonian term
    if not pauli_ops:
        # If all identities, return empty circuit
        return cirq.Circuit()
    
    hamiltonian = cirq.PauliString(pauli_ops)
    
    # Create the evolution gate
    evolution_op = cirq.PauliStringPhasor(hamiltonian, exponent=-time)
    
    # Convert to circuit
    circuit = cirq.Circuit()
    circuit.append(evolution_op)
    
    return circuit
