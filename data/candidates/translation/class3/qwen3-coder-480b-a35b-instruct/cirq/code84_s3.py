# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    # Define the U3 gate parameters (theta=0.3, phi=0.2, lambda_param=0.1)
    theta, phi, lambda_param = 0.3, 0.2, 0.1
    
    # Create the U3 matrix
    u3_matrix = np.array([
        [np.cos(theta/2), -np.exp(1j*lambda_param)*np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lambda_param))*np.cos(theta/2)]
    ])
    
    # Create a single qubit gate from the matrix
    u3_gate = cirq.MatrixGate(u3_matrix)
    
    # Create controlled version of the gate
    controlled_u3 = cirq.ControlledGate(u3_gate)
    
    # Apply the controlled gate to qubits (control=q0, target=q1)
    circuit.append(controlled_u3(qubits[0], qubits[1]))
    
    return circuit
