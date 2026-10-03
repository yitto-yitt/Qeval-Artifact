# EVAL_META: task_id=120, framework=qiskit, class=3

import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal

def create_diagonal_circuit(diag):
    """
    Create a QuantumCircuit with a Diagonal gate applied to the qubits.
    
    Args:
        diag (list): A list of complex numbers representing the diagonal elements.
        
    Returns:
        QuantumCircuit: The quantum circuit with the diagonal gate applied.
    """
    num_qubits = int(math.log2(len(diag)))
    qc = QuantumCircuit(num_qubits)
    diagonal_gate = Diagonal(diag)
    qc.append(diagonal_gate, range(num_qubits))
    return qc
