# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda import *
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Create an empty quantum circuit
    machine = init(QMachineType.CPU)
    prog = QProg()
    
    # Determine number of qubits needed
    num_qubits = len(pauli_string)
    
    # Allocate qubits
    qubits = machine.qAlloc_many(num_qubits)
    
    # Create Pauli operator matrix
    pauli_matrix = np.eye(1)
    for char in pauli_string:
        if char == 'I':
            pauli_i = np.array([[1, 0], [0, 1]], dtype=complex)
        elif char == 'X':
            pauli_i = np.array([[0, 1], [1, 0]], dtype=complex)
        elif char == 'Y':
            pauli_i = np.array([[0, -1j], [1j, 0]], dtype=complex)
        elif char == 'Z':
            pauli_i = np.array([[1, 0], [0, -1]], dtype=complex)
        pauli_matrix = np.kron(pauli_matrix, pauli_i)
    
    # Create the evolution operator: exp(-i * H * t)
    hamiltonian = pauli_matrix
    evolution_op = scipy.linalg.expm(-1j * hamiltonian * time)
    
    # Convert to QMatrixXcd format
    dim = 2 ** num_qubits
    qmat = QMatrixXcd(dim, dim)
    for i in range(dim):
        for j in range(dim):
            qmat[i, j] = evolution_op[i, j]
    
    # Create custom gate from unitary matrix
    custom_gate = matrix_decompose_qr(qmat, qubits)
    
    # Add the gate to the circuit
    prog.insert(custom_gate)
    
    # Finalize
    finalize()
    
    return prog
