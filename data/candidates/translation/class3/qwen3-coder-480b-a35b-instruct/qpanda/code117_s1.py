# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda import *
import numpy as np

def decompose_unitary(unitary):
    # Convert numpy array to QMatrixXcd format
    mat = QMatrixXcd()
    for i in range(4):
        for j in range(4):
            mat[i][j] = complex(unitary[i][j])
    
    # Decompose the unitary using CU decomposition
    prog = QProg()
    circuit = two_qubit_cus_decomposition(mat)
    
    return circuit
