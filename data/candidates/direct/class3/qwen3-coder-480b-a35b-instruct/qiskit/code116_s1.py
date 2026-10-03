# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli
from qiskit.synthesis import MatrixExponential
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Create Pauli operator from string
    pauli = Pauli(pauli_string)
    
    # Get the matrix representation
    pauli_matrix = pauli.to_matrix()
    
    # Create the evolution operator: exp(-i * time * H)
    evolution_matrix = MatrixExponential().synthesize(-1j * time * pauli_matrix)
    
    # Create quantum circuit with appropriate number of qubits
    num_qubits = len(pauli_string)
    qc = QuantumCircuit(num_qubits)
    
    # Apply the evolution gate
    qc.unitary(evolution_matrix, range(num_qubits))
    
    return qc
