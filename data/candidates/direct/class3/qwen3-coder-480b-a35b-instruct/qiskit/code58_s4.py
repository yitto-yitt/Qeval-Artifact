# EVAL_META: task_id=58, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def create_ch_gate():
    qc = QuantumCircuit(2)
    # Implement CH gate using CX and RY gates
    # H = RY(pi/2) * X * RY(-pi/2) * X
    # For controlled-Hadamard, we use the decomposition:
    qc.ry(np.pi/4, 1)
    qc.cx(0, 1)
    qc.ry(-np.pi/4, 1)
    qc.cx(0, 1)
    return qc
