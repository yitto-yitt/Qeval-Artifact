# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    c1 = np.array(data1)
    c2 = np.array(data2)
    
    adj_c1 = c1.conj().T
    
    D1 = c1.shape[0]
    d = int(np.round(np.sqrt(D1)))
    
    c1_4d = c1.reshape(d, d, d, d)
    c2_4d = c2.reshape(d, d, d, d)
    
    c12_4d = np.einsum('ikjl,kmln->imjn', c1_4d, c2_4d)
    c12 = c12_4d.reshape(d * d, d * d)
    
    return c1, adj_c1, c12
