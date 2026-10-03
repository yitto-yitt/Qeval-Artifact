# EVAL_META: task_id=108, framework=qiskit, class=3
from qiskit.quantum_info import Choi
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    # Initialize Choi matrices for data1 and data2
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    
    # Compute the adjoint of data1's Choi matrix
    choi1_adjoint = choi1.adjoint()
    
    # Compose the Choi matrices (choi1 followed by choi2)
    composed_choi = choi2.compose(choi1)
    
    # Return the data1 Choi matrix, its adjoint, and the composed Choi matrices
    return choi1, choi1_adjoint, composed_choi
