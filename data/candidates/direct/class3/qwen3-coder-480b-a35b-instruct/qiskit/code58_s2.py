# EVAL_META: task_id=58, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def create_ch_gate():
    qc = QuantumCircuit(2)
    # Apply RY(pi/4) to target qubit
    qc.ry(np.pi/4, 1)
    # Apply CX with control as q0 and target as q1
    qc.cx(0, 1)
    # Apply RY(-pi/4) to target qubit
    qc.ry(-np.pi/4, 1)
    return qc
