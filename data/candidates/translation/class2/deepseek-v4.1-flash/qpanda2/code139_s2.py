# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from pyqpanda import *

def schmidt_test(data, qargs_B):
    # Convert data to a numpy array
    if hasattr(data, 'get_matrix'):
        rho = data.get_matrix()
    elif hasattr(data, 'to_numpy'):
        rho = data.to_numpy()
    elif hasattr(data, 'data'):
        rho = data.data
    else:
        rho = np.array(data)
    
    rho = np.asarray(rho)
    
    # Determine if input is statevector or density matrix
    if rho.ndim == 1:
        psi = rho
        psi = psi / np.linalg.norm(psi)
        num_qubits = int(np.log2(len(psi)))
    elif rho.ndim == 2:
        dim = rho.shape[0]
        num_qubits = int(np.log2(dim))
        purity = np.trace(rho @ rho).real
        if not np.isclose(purity, 1.0):
            raise ValueError("Density matrix is not pure. Schmidt decomposition is not defined for mixed states.")
        evals, evecs = np.linalg.eigh(rho)
        idx = np.argmax(evals)
        psi = evecs[:, idx]
        psi = psi / np.linalg.norm(psi)
    else:
        raise ValueError("Input must be a statevector or density matrix.")
    
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(num_qubits) if i not in qargs_B]
    
    psi_tensor = psi.reshape((2,) * num_qubits)
    perm = [num_qubits - 1 - a for a in reversed(qargs_A)] + [num_qubits - 1 - b for b in reversed(qargs_B)]
    psi_permuted = np.transpose(psi_tensor, perm)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = psi_permuted.reshape((dim_A, dim_B))
    
    U, s, Vh = np.linalg.svd(mat, full_matrices=False)
    
    terms = []
    for k in range(len(s)):
        coeff = s[k]
        stateA = U[:, k]
        stateB = Vh[k, :].conj()
        terms.append((coeff, stateA, stateB))
    
    return terms
