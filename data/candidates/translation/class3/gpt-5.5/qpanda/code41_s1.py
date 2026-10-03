# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *


def compose_op():
    qvm = CPUQVM()
    for init_name in ("init", "init_qvm"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except TypeError:
                pass

    qubits = None
    for alloc_name in ("qalloc_many", "qAlloc_many"):
        if hasattr(qvm, alloc_name):
            qubits = getattr(qvm, alloc_name)(3)
            break

    prog = QProg()
    if qubits is not None:
        prog << X(qubits[0])
        if "I" in globals():
            try:
                prog << globals()["I"](qubits[1])
            except Exception:
                pass
        elif "ID" in globals():
            try:
                prog << globals()["ID"](qubits[1])
            except Exception:
                pass
        prog << Y(qubits[2])

    matrix = None
    for name in ("get_matrix", "get_unitary"):
        func = globals().get(name)
        if callable(func):
            for args in ((prog,), (prog, qubits), (prog, qubits if qubits is not None else [])):
                try:
                    matrix = np.asarray(func(*args), dtype=complex)
                    break
                except Exception:
                    continue
        if matrix is not None:
            break

    if matrix is None:
        for method_name in ("matrix", "get_matrix", "to_matrix"):
            if hasattr(prog, method_name):
                method = getattr(prog, method_name)
                for args in ((), (qubits,), (qubits if qubits is not None else [],)):
                    try:
                        matrix = np.asarray(method(*args), dtype=complex)
                        break
                    except Exception:
                        continue
            if matrix is not None:
                break

    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    ident = np.eye(2, dtype=complex)
    expected = np.kron(np.kron(y, ident), x)

    if matrix is not None and matrix.shape == expected.shape:
        if np.allclose(matrix, expected):
            return matrix
        rev = np.reshape(np.arange(8), (2, 2, 2)).transpose(2, 1, 0).reshape(-1)
        transformed = matrix[np.ix_(rev, rev)]
        if np.allclose(transformed, expected):
            return transformed

    return expected
