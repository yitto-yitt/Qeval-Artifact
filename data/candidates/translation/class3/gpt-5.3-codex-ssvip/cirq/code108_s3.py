# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)
    adjoint_choi1 = choi1.conj().T
    d_out = int(round(np.sqrt(choi1.shape[0])))
    d_in = int(round(np.sqrt(choi1.shape[1])))
    choi1_reshaped = choi1.reshape(d_out, d_in, d_out, d_in)
    choi2_reshaped = choi2.reshape(d_out, d_in, d_out, d_in)
    composed = np.einsum('aibj,bkdl->aikjdl', choi1_reshaped, choi2_reshaped).reshape(d_out * d_out, d_in * d_in)
    return choi1, adjoint_choi1, composed
