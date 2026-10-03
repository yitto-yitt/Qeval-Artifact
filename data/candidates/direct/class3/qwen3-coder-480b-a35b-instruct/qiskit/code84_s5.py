# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate
from qiskit.extensions import UnitaryGate
import numpy as np

def controlled_custom_unitary_circuit():
    # Define the custom unitary matrix using U-gate parameters (theta, phi, lam)
    theta = 0.3
    phi = 0.2
    lam = 0.1
    
    # Create the single qubit unitary gate
    u_gate = UGate(theta, phi, lam)
    
    # Create a 2-qubit quantum circuit
    qc = QuantumCircuit(2)
    
    # Add the controlled version of the custom unitary gate
    # Apply control on qubit 0, target on qubit 1
    qc.append(u_gate.control(), [0, 1])
    
    return qc
