# EVAL_META: task_id=108, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Choi

def initialize_adjoint_and_compose(data1, data2):
    # Initialize Choi matrices for data1 and data2
    choi_data1 = Choi(data1)
    choi_data2 = Choi(data2)
    
    # Compute the adjoint of data1's Choi matrix
    choi_data1_adjoint = choi_data1.adjoint()
    
    # Compose the Choi matrices (data1 and data2)
    composed_choi = choi_data1.compose(choi_data2)
    
    # Return in the specified order: data1 Choi matrix, its adjoint, and the composed Choi matrices
    return choi_data1, choi_data1_adjoint, composed_choi
