# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    # Define the custom 1-qubit unitary gate using U3 parameters (theta, phi, lambda)
    theta, phi, lam = 0.3, 0.2, 0.1
    u3_matrix = cirq.unitary(cirq.U3(theta, phi, lam))
    
    # Create a controlled version of the custom unitary
    controlled_u3 = cirq.ControlledGate(cirq.MatrixGate(u3_matrix))
    
    # Apply the controlled gate to qubits (control=0, target=1)
    circuit.append(controlled_u3(qubits[0], qubits[1]))
    
    return circuit
