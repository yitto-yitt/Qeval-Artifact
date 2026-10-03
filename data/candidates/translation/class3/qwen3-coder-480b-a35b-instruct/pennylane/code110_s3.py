# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Extract the original circuit's unitary matrix
    dev = qml.device('default.qubit', wires=circuit.num_wires)
    
    @qml.qnode(dev)
    def get_original_unitary():
        circuit.decomposition()
        return qml.state()
    
    # Get original unitary by applying to computational basis states
    original_matrix = []
    for i in range(2**circuit.num_wires):
        state = np.zeros(2**circuit.num_wires)
        state[i] = 1
        # Apply original circuit to get transformed state
        dev._state = state.astype(complex)
        result = get_original_unitary()
        original_matrix.append(result)
    original_unitary = np.array(original_matrix).T
    
    qc_list = []
    counter = 0
    
    while counter < n:
        # Generate a random Clifford operation
        new_circuit = qml.Clifford(qml.random_clifford(circuit.num_wires), wires=list(range(circuit.num_wires)))
        
        @qml.qnode(dev)
        def get_new_unitary():
            new_circuit.decomposition()
            return qml.state()
        
        # Get new unitary by applying to computational basis states
        new_matrix = []
        for i in range(2**circuit.num_wires):
            state = np.zeros(2**circuit.num_wires)
            state[i] = 1
            # Apply new circuit to get transformed state
            dev._state = state.astype(complex)
            result = get_new_unitary()
            new_matrix.append(result)
        new_unitary = np.array(new_matrix).T
        
        # Check equivalence within tolerance
        diff = np.abs(original_unitary - new_unitary)
        if np.all(diff <= 0.4 + 1e-9):  # Using absolute tolerance of 0.4
            counter += 1
            qc_list.append(new_circuit)
    
    return qc_list
