# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)
    
    adjoint_choi1 = choi1.conj().T
    
    d2 = choi1.shape[0]
    d = int(np.sqrt(d2))
    
    C1_4d = choi1.reshape(d, d, d, d)
    S1_4d = C1_4d.transpose(1, 3, 0, 2)
    S1 = S1_4d.reshape(d2, d2)
    
    C2_4d = choi2.reshape(d, d, d, d)
    S2_4d = C2_4d.transpose(1, 3, 0, 2)
    S2 = S2_4d.reshape(d2, d2)
    
    S_comp = S2 @ S1
    
    S_comp_4d = S_comp.reshape(d, d, d, d)
    C_comp_4d = S_comp_4d.transpose(2, 0, 3, 1)
    composed_choi = C_comp_4d.reshape(d2, d2)
    
    return choi1, adjoint_choi1, composed_choi
