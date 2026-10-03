# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Extract the original circuit's unitary matrix
    dev = qml.device('default.qubit', wires=circuit.num_wires)
    
    @qml.qnode(dev)
    def get_original_unitary():
        # Execute the original circuit
        for op in circuit.operations:
            qml.apply(op)
        return qml.state()
    
    # Get the original unitary by applying to computational basis states
    num_qubits = circuit.num_wires
    
    # Build the original unitary matrix by running the circuit on each basis state
    original_unitary = np.zeros((2**num_qubits, 2**num_qubits), dtype=complex)
    for i in range(2**num_qubits):
        # Prepare the i-th computational basis state
        binary_state = [int(x) for x in format(i, f'0{num_qubits}b')]
        
        # Create a temporary device and qnode to get the output state
        temp_dev = qml.device('default.qubit', wires=num_qubits)
        
        @qml.qnode(temp_dev)
        def apply_original_with_basis():
            # Prepare initial state |i>
            for j, bit in enumerate(binary_state):
                if bit == 1:
                    qml.PauliX(wires=j)
            
            # Apply original circuit operations
            for op in circuit.operations:
                qml.apply(op)
            
            return qml.state()
        
        final_state = apply_original_with_basis()
        original_unitary[:, i] = final_state
    
    # Generate equivalent Clifford circuits
    qc_list = []
    counter = 0
    
    while counter < n:
        # Generate a random Clifford operation using Pauli rotations and CNOTs
        new_circuit = qml.tape.QuantumTape()
        
        # For small systems we can generate random Clifford gates
        # We'll use a combination of Pauli gates, Hadamard, Phase and CNOTs
        with qml.tape.Tape() as tape:
            for _ in range(num_qubits * 2):  # Add some random Clifford operations
                gate_choice = np.random.randint(6)
                if gate_choice == 0 and num_qubits > 1:
                    # Add CNOT
                    control = np.random.randint(num_qubits)
                    target = np.random.choice([i for i in range(num_qubits) if i != control])
                    qml.CNOT(wires=[control, target])
                elif gate_choice == 1:
                    # Add H
                    wire = np.random.randint(num_qubits)
                    qml.Hadamard(wires=wire)
                elif gate_choice == 2:
                    # Add X
                    wire = np.random.randint(num_qubits)
                    qml.PauliX(wires=wire)
                elif gate_choice == 3:
                    # Add Y
                    wire = np.random.randint(num_qubits)
                    qml.PauliY(wires=wire)
                elif gate_choice == 4:
                    # Add Z
                    wire = np.random.randint(num_qubits)
                    qml.PauliZ(wires=wire)
                elif gate_choice == 5:
                    # Add S (Phase)
                    wire = np.random.randint(num_qubits)
                    qml.S(wires=wire)
        
        # Get the unitary of the new circuit
        temp_dev = qml.device('default.qubit', wires=num_qubits)
        
        # Build the new unitary matrix similarly
        new_unitary = np.zeros((2**num_qubits, 2**num_qubits), dtype=complex)
        for i in range(2**num_qubits):
            binary_state = [int(x) for x in format(i, f'0{num_qubits}b')]
            
            @qml.qnode(temp_dev)
            def apply_new_with_basis():
                # Prepare initial state |i>
                for j, bit in enumerate(binary_state):
                    if bit == 1:
                        qml.PauliX(wires=j)
                
                # Apply new circuit operations
                for op in tape.operations:
                    qml.apply(op)
                
                return qml.state()
            
            final_state = apply_new_with_basis()
            new_unitary[:, i] = final_state
        
        # Check equivalence within tolerance
        diff_matrix = original_unitary - new_unitary
        max_diff = np.max(np.abs(diff_matrix))
        
        # Also check if they differ by a global phase
        # Compute the trace norm of the difference
        equiv_by_global_phase = False
        for phase_angle in np.linspace(0, 2*np.pi, 100):
            phase_factor = np.exp(1j * phase_angle)
            diff_with_phase = original_unitary - phase_factor * new_unitary
            if np.max(np.abs(diff_with_phase)) <= 0.8:  # sqrt(2*0.4^2) as rough upper bound for phase tolerance
                equiv_by_global_phase = True
                break
        
        if max_diff <= 0.4 or equiv_by_global_phase:
            # Convert the tape operations to a form similar to the input
            # Since PennyLane doesn't have direct circuit representation like Qiskit,
            # we create a new tape that contains the operations
            new_tape = qml.tape.QuantumTape()
            with new_tape:
                for op in tape.operations:
                    qml.apply(op)
            
            qc_list.append(new_tape)
            counter += 1
    
    return qc_list
