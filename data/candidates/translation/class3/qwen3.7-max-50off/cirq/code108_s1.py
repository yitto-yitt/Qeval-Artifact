# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)
    
    d2 = choi1.shape[0]
    d = int(np.round(np.sqrt(d2)))
    
    C1_reshaped = choi1.reshape(d, d, d, d)
    S1 = np.transpose(C1_reshaped, (1, 3, 0, 2)).reshape(d2, d2)
    
    C2_reshaped = choi2.reshape(d, d, d, d)
    S2 = np.transpose(C2_reshaped, (1, 3, 0, 2)).reshape(d2, d2)
    
    S1_adj = S1.conj().T
    S1_adj_reshaped = S1_adj.reshape(d, d, d, d)
    adjoint_choi1 = np.transpose(S1_adj_reshaped, (2, 0, 3, 1)).reshape(d2, d2)
    
    S_comp = S1 @ S2
    S_comp_reshaped = S_comp.reshape(d, d, d, d)
    composed_choi = np.transpose(S_comp_reshaped, (2, 0, 3, 1)).reshape(d2, d2)
    
    return choi1, adjoint_choi1, composed_choi
