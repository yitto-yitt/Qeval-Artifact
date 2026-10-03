# EVAL_META: task_id=69, framework=qiskit, class=3

from qiskit import QuantumCircuit
import numpy as np

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit(2)
    
    # H gate on qubit 0
    qc.h(0)
    
    # Controlled-S gate on qubits 0 (control) and 1 (target)
    cs_matrix = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1j]])
    qc.unitary(cs_matrix, [0, 1], label='CS')
    
    # H gate on qubit 1
    qc.h(1)
    
    # Controlled-S dagger gate on qubits 1 (control) and 0 (target)
    csdg_matrix = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, -1j]])
    qc.unitary(csdg_matrix, [1, 0], label='CS†')
    
    return qc
