# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_wires = len(pauli_string)
    
    # Convert Pauli string to PennyLane observables
    observables = []
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            observables.append(qml.PauliX(i))
        elif pauli_char == 'Y':
            observables.append(qml.PauliY(i))
        elif pauli_char == 'Z':
            observables.append(qml.PauliZ(i))
        elif pauli_char == 'I':
            continue  # Identity doesn't contribute to the Hamiltonian
    
    if not observables:
        # If all identities, return identity evolution (no gates needed)
        def circuit():
            pass
        return circuit
    
    # Create tensor product of observables
    hamiltonian = observables[0]
    for obs in observables[1:]:
        hamiltonian = hamiltonian @ obs
    
    # Define the evolution circuit
    def circuit():
        qml.exp(hamiltonian, -1j * time)
    
    return circuit
