# EVAL_META: task_id=60, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def create_cy_gate():
    qc = QuantumCircuit(2)
    # Implement CY gate using CX and single-qubit gates
    # CY = (I ⊗ S) * CX * (I ⊗ S†)
    qc.sdg(1)  # Apply S† to target qubit
    qc.cx(0, 1)  # Apply CX gate
    qc.s(1)  # Apply S to target qubit
    return qc.to_instruction()
