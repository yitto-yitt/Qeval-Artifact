# EVAL_META: task_id=108, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Choi

def initialize_adjoint_and_compose(data1, data2):
    # Create Choi matrices from the input data
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    
    # Compute the adjoint of data1
    choi1_adjoint = choi1.adjoint()
    
    # Compose the Choi matrices (composition of quantum channels)
    composed_choi = choi1.compose(choi2)
    
    # Return the three Choi matrices in the specified order
    return choi1, choi1_adjoint, composed_choi
