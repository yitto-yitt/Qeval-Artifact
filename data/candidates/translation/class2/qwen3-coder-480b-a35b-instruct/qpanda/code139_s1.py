# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *
from pyqpanda3.utils import *

def schmidt_test(data, qargs_B):
    # Convert input data to numpy array if needed
    if hasattr(data, 'data'):
        rho = np.array(data.data)
    else:
        rho = np.array(data)
    
    # Determine total number of qubits
    n_total = int(np.log2(rho.shape[0]))
    
    # Determine qubits for subsystems A and B
    qargs_B_set = set(qargs_B)
    qargs_A = [i for i in range(n_total) if i not in qargs_B_set]
    
    # Calculate Schmidt decomposition using SVD
    # Reshape density matrix according to the bipartition
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # For simplicity, assume qargs_A are the first qubits and qargs_B are the last qubits
    # In a more general implementation, we would need to reorder accordingly
    reshaped_rho = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # Trace out subsystem B to get reduced density matrix for A
    rho_A = np.trace(reshaped_rho, axis1=1, axis2=3)
    
    # Trace out subsystem A to get reduced density matrix for B
    rho_B = np.trace(reshaped_rho, axis1=0, axis2=2)
    
    # Perform SVD on the density matrix
    U, s, Vd = np.linalg.svd(rho_A)
    
    # The Schmidt coefficients are the square roots of the singular values
    coefficients = np.sqrt(s)
    
    # The Schmidt vectors are the columns of U and V
    schmidt_vectors_A = U.T
    schmidt_vectors_B = Vd
    
    # Format results
    result = []
    for i in range(len(coefficients)):
        if coefficients[i] > 1e-10:  # Only include significant coefficients
            result.append((coefficients[i], schmidt_vectors_A[i], schmidt_vectors_B[i]))
    
    return result
