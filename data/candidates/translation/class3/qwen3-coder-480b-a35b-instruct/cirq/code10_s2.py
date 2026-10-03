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
    
    # Create the operation with the given unitary
    op = cirq.MatrixGate(unitary_matrix).on(q0, q1)
    
    # Decompose into single-qubit gates and CNOTs
    circuit = cirq.Circuit()
    circuit.append(cirq.decompose(op))
    
    return circuit
