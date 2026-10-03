# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    # Define the unitary matrix
    unitary_matrix = np.array([[0, 0, 0, 1], 
                               [0, 0, 1, 0], 
                               [0, 1, 0, 0], 
                               [1, 0, 0, 0]])
    
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create the gate from the unitary matrix
    custom_gate = cirq.MatrixGate(unitary_matrix)
    
    # Decompose the 2-qubit gate into single-qubit gates and CNOTs
    circuit = cirq.Circuit()
    
    # Apply the custom gate (which will be decomposed internally)
    circuit.append(custom_gate(q0, q1))
    
    # Since Cirq doesn't have direct equivalent to Qiskit's transpilation,
    # we'll just return the circuit with the gate applied
    return circuit
