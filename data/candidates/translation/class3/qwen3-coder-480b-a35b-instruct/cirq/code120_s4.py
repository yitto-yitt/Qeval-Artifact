# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    n_qubits = int(np.log2(len(diag)))
    qubits = [cirq.LineQubit(i) for i in range(n_qubits)]
    
    # Create diagonal matrix
    diag_matrix = np.diag(diag)
    
    # Create a custom gate from the diagonal matrix
    diagonal_gate = cirq.MatrixGate(diag_matrix)
    
    circuit = cirq.Circuit()
    circuit.append(diagonal_gate(*qubits))
    
    return circuit
