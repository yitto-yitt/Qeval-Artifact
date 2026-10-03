# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def calculate_phase_difference_fidelity():
    # Create the first operator - Hadamard gate
    op_a_matrix = qml.matrix(qml.Hadamard(wires=0))
    
    # Create the second operator - Hadamard gate with global phase
    h_gate_matrix = qml.matrix(qml.Hadamard(wires=0))
    op_b_matrix = np.exp(1j * 0.5) * h_gate_matrix
    
    # Calculate process fidelity using pennylane's quantum function approach
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def process_fidelity_circuit():
        # Prepare ancilla and system qubits
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        
        # Apply first operation to system (controlled by ancilla)
        qml.ctrl(qml.QubitUnitary, control=0)(op_a_matrix.reshape((2, 2)), wires=1)
        
        # Apply adjoint of second operation to system (controlled by ancilla)
        qml.ctrl(qml.QubitUnitary, control=0)(np.conj(op_b_matrix.T).reshape((2, 2)), wires=1)
        
        # Undo entangling operation
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        
        return qml.probs(wires=0)
    
    probs = process_fidelity_circuit()
    fidelity = probs[0]  # Probability of measuring |0> on ancilla
    return fidelity
