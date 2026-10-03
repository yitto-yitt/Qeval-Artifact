# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    # Create two qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Decompose the unitary using cirq's two-qubit decomposition
    operations = cirq.two_qubit_matrix_to_operations(q0, q1, unitary)
    
    # Create a circuit with the decomposed operations
    circuit = cirq.Circuit(operations)
    
    return circuit
