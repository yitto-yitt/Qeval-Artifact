# EVAL_META: task_id=139, framework=qiskit, class=2

import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix

def schmidt_test(data, qargs_B):
    """
    Return the Schmidt decomposition coefficients and subsystem vectors 
    for the given density matrix/statevector and partition.
    """
    # Extract state vector from the input data
    if isinstance(data, DensityMatrix):
        eigvals, eigvecs = np.linalg.eigh(data.data)
        idx = np.argmax(eigvals)
        psi = eigvecs[:, idx]
    elif isinstance(data, Statevector):
        psi = data.data
    elif isinstance(data, np.ndarray):
        if data.ndim == 2:
            eigvals, eigvecs = np.linalg.eigh(data)
            idx = np.argmax(eigvals)
            psi = eigvecs[:, idx]
        else:
            psi = data
    else:
        try:
            psi = Statevector(data).data
        except Exception:
            dm = DensityMatrix(data)
            eigvals, eigvecs = np.linalg.eigh(dm.data)
            idx = np.argmax(eigvals)
            psi = eigvecs[:, idx]

    num_qubits = int(np.round(np.log2(len(psi))))
    tensor = psi.reshape([2] * num_qubits)
    
    # Map qubit indices to tensor axes (Qiskit uses little-endian ordering)
    axes_B = [num_qubits - 1 - k for k in qargs_B]
    axes_A = [num_qubits - 1 - k for k in range(num_qubits) if k not in qargs_B]
    
    # Transpose and reshape to 2D matrix
    tensor_transposed = tensor.transpose(axes_A + axes_B)
    dim_A = 2**len(axes_A)
    dim_B = 2**len(axes_B)
    matrix = tensor_transposed.reshape(dim_A, dim_B)
    
    # Perform SVD
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    # Build the list of Schmidt terms
    terms = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vh[i, :]
        terms.append((coeff, state_A, state_B))
        
    return terms
