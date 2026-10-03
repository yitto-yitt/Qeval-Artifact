# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *
from pyqpanda3.algorithm import *

def schmidt_test(data, qargs_B):
    # Convert the input data to a numpy array if it's not already
    density_matrix = np.array(data)
    
    # Get dimensions
    dim = density_matrix.shape[0]
    n_qubits = int(np.log2(dim))
    
    # Determine qubits for partition A based on qargs_B
    all_qubits = list(range(n_qubits))
    qargs_A = [q for q in all_qubits if q not in qargs_B]
    
    # Calculate dimensions of partitions
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Reshape the density matrix to perform SVD for Schmidt decomposition
    # Reshape as matrix where rows correspond to partition A and columns to partition B
    reshaped_matrix = density_matrix.reshape((dim_A, dim_B))
    
    # Perform SVD
    U, singular_values, Vh = np.linalg.svd(reshaped_matrix, full_matrices=False)
    
    # Prepare results
    result = []
    for i in range(len(singular_values)):
        coeff = singular_values[i]
        state_A = U[:, i]
        state_B = Vh[i, :]  # This is already conjugated in SVD
        
        result.append([coeff, state_A.tolist(), state_B.tolist()])
    
    return result
