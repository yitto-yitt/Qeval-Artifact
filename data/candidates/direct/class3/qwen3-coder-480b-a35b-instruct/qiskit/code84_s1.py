# EVAL_META: task_id=84, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def controlled_custom_unitary_circuit():
    # Define the angles
    alpha, beta, gamma = 0.3, 0.2, 0.1
    
    # Create the unitary matrix for the custom gate
    # Using the standard Euler angle decomposition: Rz(alpha) * Ry(beta) * Rz(gamma)
    cos_beta_2 = np.cos(beta/2)
    sin_beta_2 = np.sin(beta/2)
    
    U = np.array([
        [np.exp(-1j*(alpha+gamma)/2) * cos_beta_2, -np.exp(-1j*(alpha-gamma)/2) * sin_beta_2],
        [np.exp(1j*(alpha-gamma)/2) * sin_beta_2, np.exp(1j*(alpha+gamma)/2) * cos_beta_2]
    ])
    
    # Create a quantum circuit with 2 qubits
    qc = QuantumCircuit(2)
    
    # Define the custom unitary gate
    custom_gate = Operator(U)
    
    # Create the controlled version of the custom gate
    controlled_custom_gate = custom_gate.control(1)
    
    # Apply the controlled gate with qubit 0 as control and qubit 1 as target
    qc.append(controlled_custom_gate, [0, 1])
    
    return qc
