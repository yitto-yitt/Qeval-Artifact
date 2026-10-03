# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)
    
    adjoint_choi1 = choi1.conj().T
    
    d1 = int(np.sqrt(choi1.shape[0]))
    d2 = int(np.sqrt(choi2.shape[0]))
    
    A = choi1.reshape(d1, d1, d1, d1)
    B = choi2.reshape(d2, d2, d2, d2)
    
    C = np.einsum('m k n l, i m j n -> i k j l', A, B)
    
    d_in = d2
    d_out = d1
    composed_choi = C.reshape(d_in * d_out, d_in * d_out)
    
    return choi1, adjoint_choi1, composed_choi
