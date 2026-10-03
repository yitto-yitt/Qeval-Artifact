# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    
    # Convert the 4x4 unitary to a cirq operation
    operation = cirq.MatrixGate(unitary).on(*qubits)
    
    # Decompose using cirq's built-in two-qubit decomposition
    decomposed_ops = cirq.two_qubit_matrix_to_operations(qubits[0], qubits[1], unitary)
    
    circuit.append(decomposed_ops)
    
    return circuit
