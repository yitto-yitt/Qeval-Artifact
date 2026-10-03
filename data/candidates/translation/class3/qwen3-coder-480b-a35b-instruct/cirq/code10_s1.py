# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    # Define the unitary matrix
    unitary_matrix = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ])
    
    # Create a two-qubit gate from the unitary matrix
    custom_gate = cirq.MatrixGate(unitary_matrix)
    
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create the circuit with the custom gate
    circuit = cirq.Circuit(custom_gate(q0, q1))
    
    # Transpile (optimize) the circuit using Cirq's default optimizers
    # Since Cirq doesn't have explicit optimization levels like Qiskit,
    # we'll use a standard set of optimizers to achieve similar results
    optimized_circuit = cirq.optimize_for_target_gateset(
        circuit,
        gateset=cirq.CZTargetGateset()
    )
    
    # Decompose into single-qubit gates and CNOTs (CX)
    decomposed_circuit = cirq.decompose_to_single_qubit_operations_and_bare_cnots(
        optimized_circuit
    )
    
    return decomposed_circuit
