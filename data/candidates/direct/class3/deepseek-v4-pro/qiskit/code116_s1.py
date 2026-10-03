# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    """
    Synthesizes an evolution gate for a given Pauli string and time using matrix exponential.

    Args:
        pauli_string (str): A string consisting of 'I', 'X', 'Y', 'Z' characters.
        time (float): Evolution time.

    Returns:
        QuantumCircuit: A circuit implementing the evolution operator exp(-i * time * H),
                        where H is the tensor product of the Pauli matrices.
    """
    n = len(pauli_string)
    
    # Single-qubit Pauli matrices
    pauli_map = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }
    
    # Build Hamiltonian as tensor product of individual Paulis
    # Tensor order matches qiskit: qubit 0 ⊗ qubit 1 ⊗ ... (left to right in string)
    H = pauli_map[pauli_string[0]]
    for char in pauli_string[1:]:
        H = np.kron(H, pauli_map[char])
    
    # Compute matrix exponential
    U = expm(-1j * time * H)
    
    # Create quantum circuit with the unitary evolution
    qc = QuantumCircuit(n)
    qc.unitary(U, range(n))
    
    return qc
