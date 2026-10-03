# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_wires = len(pauli_strings[0])
    dev = qml.device('default.qubit', wires=n_wires)
    
    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            # Convert the Pauli string to PennyLane format
            observables = []
            for i, pauli_char in enumerate(pauli_string):
                if pauli_char == 'X':
                    observables.append(qml.PauliX(i))
                elif pauli_char == 'Y':
                    observables.append(qml.PauliY(i))
                elif pauli_char == 'Z':
                    observables.append(qml.PauliZ(i))
                else:  # Identity
                    continue
            
            if observables:
                # Create tensor product of observables
                if len(observables) == 1:
                    hamiltonian = observables[0]
                else:
                    hamiltonian = observables[0] @ observables[1] if len(observables) == 2 else observables[0]
                    for obs in observables[2:]:
                        hamiltonian = hamiltonian @ obs
                
                # Apply Trotterized evolution - for reps > 1 we repeat the evolution
                for _ in range(reps):
                    qml.ApproxTimeEvolution(hamiltonian, time / reps, 1)
        
        return qml.state()
    
    # Build the tape to get operations
    tape = circuit.qtape
    
    # Create a new device to execute the operations
    new_dev = qml.device('default.qubit', wires=n_wires)
    
    @qml.qnode(new_dev)
    def build_circuit():
        for op in tape.operations:
            qml.apply(op)
        return qml.state()
    
    build_circuit()
    
    # Return the quantum tape which contains the operations
    return build_circuit.qtape
