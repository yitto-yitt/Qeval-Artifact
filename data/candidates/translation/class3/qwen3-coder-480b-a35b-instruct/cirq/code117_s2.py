# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    # Create two qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Decompose the 4x4 unitary into a circuit using CNOT as the basis gate
    operations = cirq.two_qubit_matrix_to_operations(q0, q1, unitary, allow_partial_czs=False)
    
    # Create a circuit from the operations
    circuit = cirq.Circuit(operations)
    
    return circuit
