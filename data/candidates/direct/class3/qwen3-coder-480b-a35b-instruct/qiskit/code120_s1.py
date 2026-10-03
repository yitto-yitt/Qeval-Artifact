# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def create_diagonal_circuit(diag):
    # Create a quantum circuit with the number of qubits needed to represent the diagonal elements
    num_qubits = int(np.log2(len(diag)))
    qc = QuantumCircuit(num_qubits)
    
    # Apply the diagonal gate
    qc.diagonal(diag, range(num_qubits))
    
    return qc
