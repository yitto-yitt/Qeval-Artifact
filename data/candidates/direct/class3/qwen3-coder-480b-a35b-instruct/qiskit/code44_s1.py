# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def tensor_circuits():
    # Create 1-qubit circuit with X gate
    qc1 = QuantumCircuit(1)
    qc1.x(0)
    
    # Create 2-qubit circuit with CRY gate
    qc2 = QuantumCircuit(2)
    qc2.cry(0.2, 0, 1)
    
    # Tensor product with qc2 first (2-qubit) then qc1 (1-qubit)
    # This results in a 3-qubit circuit
    qc = qc2.tensor(qc1)
    
    return qc
