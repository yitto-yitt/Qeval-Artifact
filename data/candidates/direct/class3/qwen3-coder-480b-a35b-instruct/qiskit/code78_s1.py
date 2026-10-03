# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    
    for i in range(num_qubits):
        qc.h(i)
        for j in range(i + 1, num_qubits):
            qc.cp(np.pi / 2**(j - i), j, i)
    
    return qc.inverse()
