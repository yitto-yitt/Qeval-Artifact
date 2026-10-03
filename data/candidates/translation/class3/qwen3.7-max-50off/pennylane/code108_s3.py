# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    c1 = np.array(data1, dtype=complex)
    c2 = np.array(data2, dtype=complex)
    
    adj_c1 = c1.conj().T
    
    d2 = c1.shape[0]
    d = int(np.round(np.sqrt(d2)))
    
    if d * d == d2:
        C1_t = c1.reshape(d, d, d, d)
        S1_t = np.transpose(C1_t, (1, 3, 0, 2))
        S1 = S1_t.reshape(d2, d2)
        
        C2_t = c2.reshape(d, d, d, d)
        S2_t = np.transpose(C2_t, (1, 3, 0, 2))
        S2 = S2_t.reshape(d2, d2)
        
        S_comp = S2 @ S1
        S_comp_t = S_comp.reshape(d, d, d, d)
        C_comp_t = np.transpose(S_comp_t, (2, 0, 3, 1))
        c_comp = C_comp_t.reshape(d2, d2)
    else:
        c_comp = c2 @ c1
        
    return c1, adj_c1, c_comp
