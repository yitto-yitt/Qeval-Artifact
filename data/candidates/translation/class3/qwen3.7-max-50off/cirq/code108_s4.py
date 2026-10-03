# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq

def initialize_adjoint_and_compose(data1, data2):
    def get_choi(data):
        data = np.array(data, dtype=complex)
        try:
            cirq.choi_to_kraus(data)
            return data
        except Exception:
            dim = data.shape[0]
            C = np.zeros((dim*dim, dim*dim), dtype=complex)
            for i in range(dim):
                for j in range(dim):
                    op1 = np.zeros((dim, dim))
                    op1[i, j] = 1.0
                    op2 = data @ op1 @ data.conj().T
                    C += np.kron(op1, op2)
            return C

    choi1 = get_choi(data1)
    choi2 = get_choi(data2)
    
    adjoint_choi1 = choi1.conj().T
    
    kraus1 = cirq.choi_to_kraus(choi1)
    kraus2 = cirq.choi_to_kraus(choi2)
    
    composed_kraus = [k2 @ k1 for k1 in kraus1 for k2 in kraus2]
    composed_choi = cirq.kraus_to_choi(composed_kraus)
    
    return choi1, adjoint_choi1, composed_choi
