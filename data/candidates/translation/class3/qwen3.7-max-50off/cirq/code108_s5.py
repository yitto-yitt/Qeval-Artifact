# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np

def initialize_adjoint_and_compose(data1, data2):
    def to_choi(data):
        if isinstance(data, (list, tuple)):
            return cirq.kraus_to_choi(data)
        if isinstance(data, np.ndarray):
            if data.ndim == 3:
                return cirq.kraus_to_choi(data)
            elif data.ndim == 2:
                d = data.shape[0]
                if data.shape[0] == data.shape[1] and np.allclose(data @ data.conj().T, np.eye(d)):
                    return cirq.kraus_to_choi([data])
                return data
        try:
            kraus = cirq.kraus(data)
            return cirq.kraus_to_choi(kraus)
        except TypeError:
            pass
        return data

    choi1 = to_choi(data1)
    choi2 = to_choi(data2)
    
    kraus1 = cirq.choi_to_kraus(choi1)
    adj_kraus1 = [k.conj().T for k in kraus1]
    adjoint_choi1 = cirq.kraus_to_choi(adj_kraus1)
    
    kraus2 = cirq.choi_to_kraus(choi2)
    composed_kraus = [k1 @ k2 for k1 in kraus1 for k2 in kraus2]
    composed_choi = cirq.kraus_to_choi(composed_kraus)
    
    return choi1, adjoint_choi1, composed_choi
