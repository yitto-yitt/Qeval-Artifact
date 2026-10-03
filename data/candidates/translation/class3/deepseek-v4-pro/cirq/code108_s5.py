# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq

def initialize_adjoint_and_compose(data1, data2):
    # Convert input data to numpy arrays
    mat1 = np.array(data1)
    mat2 = np.array(data2)
    
    # Choi matrix is the data itself when provided as a matrix
    choi1 = mat1
    choi2 = mat2
    
    # Adjoint (conjugate transpose) of choi1
    adjoint_choi1 = np.conj(choi1.T)
    
    # For quantum channels, compose in Cirq corresponds to matrix multiplication
    # assuming the Choi matrices represent channels in the same convention
    composed_choi = choi1 @ choi2
    
    return choi1, adjoint_choi1, composed_choi
