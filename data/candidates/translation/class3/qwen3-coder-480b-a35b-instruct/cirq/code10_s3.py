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
    
    # Create the operation using MatrixGate
    gate = cirq.MatrixGate(unitary_matrix)
    op = gate(q0, q1)
    
    # Create the circuit
    circuit = cirq.Circuit(op)
    
    return circuit
