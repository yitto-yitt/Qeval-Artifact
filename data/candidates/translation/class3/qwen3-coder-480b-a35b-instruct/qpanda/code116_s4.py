# EVAL_META: task_id=116, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Create a quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(len(pauli_string))
    
    # Create circuit
    circuit = pq.QCircuit()
    
    # Process each pauli operator in the string
    for i, pauli_op in enumerate(pauli_string):
        if pauli_op == 'X':
            # For X rotation: exp(-i * time * X/2) = RY(pi/2) * RZ(-time) * RY(-pi/2)
            circuit.insert(pq.RY(qubits[i], np.pi / 2))
            circuit.insert(pq.RZ(qubits[i], -time))
            circuit.insert(pq.RY(qubits[i], -np.pi / 2))
        elif pauli_op == 'Y':
            # For Y rotation: exp(-i * time * Y/2) = RX(time)
            circuit.insert(pq.RX(qubits[i], time))
        elif pauli_op == 'Z':
            # For Z rotation: exp(-i * time * Z/2) = RZ(time)
            circuit.insert(pq.RZ(qubits[i], time))
        # For 'I', we do nothing
    
    # Since the evolution is tensor product of individual pauli terms,
    # we need to account for the combined effect properly
    # In case of multiple non-identity paulis, we need to consider their tensor product
    # For now, implementing a general approach for single pauli terms
    
    # If there's more than one non-identity pauli, we need special handling
    non_identity_indices = []
    for i, op in enumerate(pauli_string):
        if op != 'I':
            non_identity_indices.append(i)
    
    # If there are multiple non-identity operators, we need to implement 
    # the tensor product evolution properly
    if len(non_identity_indices) > 1:
        # For multi-qubit pauli evolution, we use trotterization concept
        # But for exact synthesis, we decompose based on the structure
        # Reset the circuit for proper multi-pauli handling
        circuit = pq.QCircuit()
        
        # Find which qubits have non-trivial operations
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op == 'X':
                # Transform X to Z basis: H-X-H = Z, so H-RZ-H
                circuit.insert(pq.H(qubits[i]))
                circuit.insert(pq.RZ(qubits[i], -time))
                circuit.insert(pq.H(qubits[i]))
            elif pauli_op == 'Y':
                # Transform Y to Z basis: Rx(pi/2)-Z-Rx(-pi/2) 
                circuit.insert(pq.RX(qubits[i], np.pi / 2))
                circuit.insert(pq.RZ(qubits[i], -time))
                circuit.insert(pq.RX(qubits[i], -np.pi / 2))
            elif pauli_op == 'Z':
                circuit.insert(pq.RZ(qubits[i], -time))
            # Identity does nothing
    
    # If only identity operators, return empty circuit
    elif len(non_identity_indices) == 0:
        circuit = pq.QCircuit()
    
    # Otherwise handle single pauli case
    else:
        circuit = pq.QCircuit()
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op == 'X':
                circuit.insert(pq.H(qubits[i]))
                circuit.insert(pq.RZ(qubits[i], -time))
                circuit.insert(pq.H(qubits[i]))
            elif pauli_op == 'Y':
                circuit.insert(pq.RX(qubits[i], np.pi / 2))
                circuit.insert(pq.RZ(qubits[i], -time))
                circuit.insert(pq.RX(qubits[i], -np.pi / 2))
            elif pauli_op == 'Z':
                circuit.insert(pq.RZ(qubits[i], -time))
    
    return circuit
