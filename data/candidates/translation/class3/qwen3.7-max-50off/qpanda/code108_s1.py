# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    C1 = np.array(data1, dtype=complex)
    C2 = np.array(data2, dtype=complex)
    
    d2 = C1.shape[0]
    d = int(np.sqrt(d2))
    
    adj_C1 = C1.conj().T
    
    S1 = C1.reshape((d, d, d, d)).transpose((1, 3, 0, 2)).reshape((d2, d2))
    S2 = C2.reshape((d, d, d, d)).transpose((1, 3, 0, 2)).reshape((d2, d2))
    
    S_comp = S1 @ S2
    
    C_comp = S_comp.reshape((d, d, d, d)).transpose((2, 0, 3, 1)).reshape((d2, d2))
    
    return C1, adj_C1, C_comp
