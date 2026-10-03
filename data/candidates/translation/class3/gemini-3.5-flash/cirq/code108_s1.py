# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1)
    choi2 = np.asarray(data2)

    d = int(np.round(np.sqrt(choi1.shape[0])))

    # Compute adjoint of choi1
    choi1_tensor = choi1.reshape(d, d, d, d)
    adjoint_choi1_tensor = np.conj(np.transpose(choi1_tensor, (1, 0, 3, 2)))
    adjoint_choi1 = adjoint_choi1_tensor.reshape(d**2, d**2)

    # Compute composition of choi1 and choi2
    choi2_tensor = choi2.reshape(d, d, d, d)
    composed_choi_tensor = np.einsum(
        "ixjy,xzyw->izjw", choi1_tensor, choi2_tensor
    )
    composed_choi = composed_choi_tensor.reshape(d**2, d**2)

    return choi1, adjoint_choi1, composed_choi
