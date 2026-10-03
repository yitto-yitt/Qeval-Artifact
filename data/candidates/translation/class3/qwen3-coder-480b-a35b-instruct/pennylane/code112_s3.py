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
                    hamiltonian = observables[0] @ observables[1]
                    for obs in observables[2:]:
                        hamiltonian = hamiltonian @ obs
                
                # Apply Trotterized evolution - Lie-Trotter corresponds to order=1
                if order == 1:
                    # Simple Trotter step
                    for _ in range(reps):
                        qml.exp(-1j * time / reps * hamiltonian)
                else:
                    # For higher orders, we use more complex trotterization
                    # But for Lie-Trotter specifically, we use first order
                    for _ in range(reps):
                        qml.exp(-1j * time / reps * hamiltonian)
        
        return qml.state()
    
    # We need to build the circuit manually using PennyLane operations
    # Since PennyLane doesn't have direct Lie-Trotter synthesis like Qiskit
    
    def build_circuit():
        for pauli_string, time in zip(pauli_strings, times):
            # Decompose the Pauli string evolution
            ops = []
            for i, pauli_char in enumerate(pauli_string):
                if pauli_char == 'X':
                    # For X rotation, we use H-Rz-H decomposition
                    qml.Hadamard(wires=i)
                    ops.append(('Z', i))
                elif pauli_char == 'Y':
                    # For Y rotation, we use Rz(pi/2)-H-Rz(pi/2) decomposition
                    qml.RZ(np.pi/2, wires=i)
                    qml.Hadamard(wires=i)
                    ops.append(('Z', i))
                elif pauli_char == 'Z':
                    # Z is already diagonal
                    ops.append(('Z', i))
            
            # Apply the rotation
            if ops:
                for _ in range(reps):
                    # Apply rotation around Z axis (after basis change)
                    angle = -time / reps
                    for pauli_op, wire in ops:
                        if pauli_op == 'Z':
                            qml.RZ(angle, wires=wire)
            
            # Undo basis changes if needed
            for i, pauli_char in enumerate(pauli_string):
                if pauli_char == 'X':
                    qml.Hadamard(wires=i)
                elif pauli_char == 'Y':
                    qml.Hadamard(wires=i)
                    qml.RZ(-np.pi/2, wires=i)
    
    # Create an empty tape to hold our operations
    with qml.tape.QuantumTape() as tape:
        build_circuit()
    
    # Create a device and qnode that applies the tape
    dev = qml.device('default.qubit', wires=n_wires)
    
    @qml.qnode(dev)
    def full_circuit():
        qml.apply(tape.operations)
        return qml.state()
    
    # Actually execute to get the circuit built
    full_circuit()
    
    # Return the tape which contains the operations
    return tape

# A simpler approach using qml.evolve and decomposing manually
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_wires = len(pauli_strings[0])
    dev = qml.device('default.qubit', wires=n_wires)
    
    def circuit_fn():
        for pauli_string, time in zip(pauli_strings, times):
            # Build the Hamiltonian from the Pauli string
            coeffs = [1.0]
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
                # Create the tensor product observable
                if len(observables) > 1:
                    obs = observables[0]
                    for o in observables[1:]:
                        obs = obs @ o
                else:
                    obs = observables[0]
                
                hamiltonian = qml.Hamiltonian([1.0], [obs])
                
                # Apply Lie-Trotter evolution
                for _ in range(reps):
                    qml.exp(qml.Identity(0), coeff=-1j * time / reps, h=hamiltonian)
            else:
                # If all identities, no evolution needed
                pass
    
    # Create tape by executing the function in a tape context
    with qml.tape.QuantumTape() as tape:
        circuit_fn()
    
    return tape
