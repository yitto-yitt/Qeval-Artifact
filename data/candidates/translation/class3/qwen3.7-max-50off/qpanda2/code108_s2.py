# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, qAlloc_many

machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(2)

def to_choi(mat):
    mat = np.array(mat, dtype=complex)
    if mat.ndim == 2 and mat.shape[0] == mat.shape[1]:
        if np.allclose(mat @ mat.conj().T, np.eye(mat.shape[0])):
            vec = mat.flatten('F')
            return np.outer(vec, vec.conj())
    return mat

def choi_to_super(C):
    d = int(np.sqrt(C.shape[0]))
    C_res = C.reshape(d, d, d, d)
    S_res = C_res.transpose(1, 3, 0, 2)
    return S_res.reshape(d*d, d*d)

def super_to_choi(S):
    d = int(np.sqrt(S.shape[0]))
    S_res = S.reshape(d, d, d, d)
    C_res = S_res.transpose(2, 0, 3, 1)
    return C_res.reshape(d*d, d*d)

def initialize_adjoint_and_compose(data1, data2):
    C1 = to_choi(data1)
    C2 = to_choi(data2)
    
    S1 = choi_to_super(C1)
    S_adj = S1.conj().T
    C_adj = super_to_choi(S_adj)
    
    S2 = choi_to_super(C2)
    S_comp = S2 @ S1
    C_comp = super_to_choi(S_comp)
    
    return C1, C_adj, C_comp

machine.finalize()
