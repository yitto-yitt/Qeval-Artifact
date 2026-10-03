# EVAL_META: task_id=4, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.circuit.library import UnitaryGate

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0],
                       [0, 1, 0, 0]])
    
    # Create a unitary gate from the matrix
    unitary_gate = UnitaryGate(matrix)
    
    # Create a quantum circuit with 2 qubits
    qc = QuantumCircuit(2)
    
    # Apply the unitary gate to the circuit
    qc.append(unitary_gate, [0, 1])
    
    return qc
