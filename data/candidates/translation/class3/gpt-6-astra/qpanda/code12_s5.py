# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    circuit = pq.QCircuit()
    circuit << pq.H(0) << pq.CNOT(0, 1)
    program = pq.QProg()
    program << circuit

    names = ("get_matrix", "get_unitary", "get_unitary_matrix", "matrix", "unitary")
    for obj in (program, circuit):
        for name in names:
            method = getattr(obj, name, None)
            if method is None:
                continue
            try:
                matrix = method() if callable(method) else method
                matrix = np.asarray(matrix, dtype=complex)
                if matrix.size == 16:
                    return matrix.reshape(4, 4)
            except (TypeError, ValueError, RuntimeError):
                continue

    for name in names:
        method = getattr(pq, name, None)
        if not callable(method):
            continue
        for obj in (program, circuit):
            try:
                matrix = np.asarray(method(obj), dtype=complex)
                if matrix.size == 16:
                    return matrix.reshape(4, 4)
            except (TypeError, ValueError, RuntimeError):
                continue

    raise RuntimeError("The framework did not expose a usable circuit-matrix operation.")
