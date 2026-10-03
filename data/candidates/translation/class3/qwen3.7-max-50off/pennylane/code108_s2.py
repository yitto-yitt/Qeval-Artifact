# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def initialize_adjoint_and_compose(data1, data2):
    c1 = np.array(data1, dtype=complex)
    c2 = np.array(data2, dtype=complex)
    
    adjoint_c1 = c1.conj().T
    
    d2 = c1.shape[0]
    d = int(np.sqrt(d2))
    
    c1_reshaped = c1.reshape((d, d, d, d))
    c2_reshaped = c2.reshape((d, d, d, d))
    
    composed_reshaped = np.einsum('ikjl,kmln->ijmn', c1_reshaped, c2_reshaped)
    composed_c = composed_reshaped.reshape((d2, d2))
    
    return c1, adjoint_c1, composed_c
