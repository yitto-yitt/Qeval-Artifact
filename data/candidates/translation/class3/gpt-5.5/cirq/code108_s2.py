# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    def _choi_array(data):
        arr = np.asarray(data, dtype=complex)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError("Choi data must be a square matrix.")
        dim = int(round(np.sqrt(arr.shape[0])))
        if dim * dim != arr.shape[0]:
            raise ValueError("Choi matrix dimension must be a perfect square.")
        return np.array(arr, dtype=complex, copy=True), dim

    choi1, dim1 = _choi_array(data1)
    choi2, dim2 = _choi_array(data2)

    if dim1 != dim2:
        raise ValueError("Choi matrices must have compatible dimensions.")

    choi1_tensor = choi1.reshape(dim1, dim1, dim1, dim1)
    choi2_tensor = choi2.reshape(dim2, dim2, dim2, dim2)

    adjoint_choi1 = (
        np.conjugate(choi1_tensor)
        .transpose(1, 0, 3, 2)
        .reshape(choi1.shape)
    )

    composed_choi = np.einsum(
        "imjn,manb->iajb",
        choi1_tensor,
        choi2_tensor,
        optimize=True,
    ).reshape(choi1.shape)

    return choi1, adjoint_choi1, composed_choi
