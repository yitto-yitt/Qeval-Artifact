# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    # Create Choi matrices from the input data
    choi1 = cirq.qis.ChiMatrix(data1, atol=1e-10)
    choi2 = cirq.qis.ChiMatrix(data2, atol=1e-10)
    
    # Compute the adjoint of choi1
    # For a Choi matrix, the adjoint is the conjugate transpose
    adjoint_data1 = np.conj(choi1.matrix).T
    adjoint_choi1 = cirq.qis.ChiMatrix(adjoint_data1, atol=1e-10)
    
    # Compose the two Choi matrices
    # In Cirq, we can compose by multiplying the matrices
    composed_data = choi1.matrix @ choi2.matrix
    composed_choi = cirq.qis.ChiMatrix(composed_data, atol=1e-10)
    
    return choi1, adjoint_choi1, composed_choi
