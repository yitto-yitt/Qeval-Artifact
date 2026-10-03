# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix.")

    for name in ("two_qubit_decompose", "kak_decompose", "matrix_decompose"):
        decomposer = getattr(pq, name, None)
        if decomposer is not None:
            documentation = decomposer.__doc__ or ""
            if "is_positive_seq" in documentation:
                return decomposer([0, 1], matrix, is_positive_seq=False)
            return decomposer([0, 1], matrix)

    raise RuntimeError("The installed pyqpanda3.core has no unitary decomposer.")
