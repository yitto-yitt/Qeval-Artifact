# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_wires = len(pauli_strings[0])
    dev = qml.device('default.qubit', wires=n_wires)
    
    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            # Convert the Pauli string to PennyLane operations
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
                # For Lie-Trotter we treat each term separately (order=1)
                hamiltonian = qml.Hamiltonian([time] * len(observables), observables)
                
                # Apply Trotterized evolution - for reps > 1, repeat the sequence
                for _ in range(reps):
                    for obs_idx in range(len(observables)):
                        coeff = time / reps if reps > 0 else time
                        # Apply the evolution for each Pauli term
                        if isinstance(observables[obs_idx], qml.PauliX):
                            wire = observables[obs_idx].wires[0]
                            qml.RX(2 * coeff, wires=wire)
                        elif isinstance(observables[obs_idx], qml.PauliY):
                            wire = observables[obs_idx].wires[0]
                            qml.RY(2 * coeff, wires=wire)
                        elif isinstance(observables[obs_idx], qml.PauliZ):
                            wire = observables[obs_idx].wires[0]
                            qml.RZ(2 * coeff, wires=wire)
        
        return qml.state()
    
    # We need to build the actual tape/operations without executing
    tape = qml.transforms.make_tape(circuit)()
    
    # Create a new device and qnode to hold our operations
    dev = qml.device('default.qubit', wires=n_wires)
    
    @qml.qnode(dev)
    def build_circuit():
        for pauli_string, time in zip(pauli_strings, times):
            # Process each Pauli string
            ops_to_apply = []
            for i, pauli_char in enumerate(pauli_string):
                if pauli_char == 'X':
                    ops_to_apply.append(qml.PauliX(i))
                elif pauli_char == 'Y':
                    ops_to_apply.append(qml.PauliY(i))
                elif pauli_char == 'Z':
                    ops_to_apply.append(qml.PauliZ(i))
            
            # Apply Trotterization
            for _ in range(reps):
                for op in ops_to_apply:
                    if isinstance(op, qml.PauliX):
                        qml.RX(2 * time / reps, wires=op.wires[0])
                    elif isinstance(op, qml.PauliY):
                        qml.RY(2 * time / reps, wires=op.wires[0])
                    elif isinstance(op, qml.PauliZ):
                        qml.RZ(2 * time / reps, wires=op.wires[0])
        
        return qml.state()
    
    # Execute once to build the tape
    build_circuit()
    
    # Return the operations from the device
    ops = dev._circuit.operations
    
    # Actually we want to return a QNode that represents the circuit
    return build_circuit
