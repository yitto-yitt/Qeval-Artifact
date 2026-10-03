# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq

def decompose_unitary(unitary):
    mat = np.asarray(unitary, dtype=np.complex128)

    qvm = pq.CPUQVM()
    for init_name in ("init_qvm", "init", "initQVM"):
        init_fn = getattr(qvm, init_name, None)
        if callable(init_fn):
            try:
                init_fn()
                break
            except TypeError:
                pass

    alloc_fn = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        alloc_fn = getattr(qvm, alloc_name, None)
        if callable(alloc_fn):
            break
    if alloc_fn is None:
        raise AttributeError("No compatible qubit allocation method found in pyqpanda3 CPUQVM")

    qubits = alloc_fn(2)

    decompose_fn = None
    for name in ("matrix_decompose", "MatrixDecompose", "unitary_decompose", "UnitaryDecompose"):
        decompose_fn = getattr(pq, name, None)
        if callable(decompose_fn):
            break
    if decompose_fn is None:
        raise AttributeError("No compatible unitary/matrix decomposition function found in pyqpanda3.core")

    attempts = (
        (qubits, mat),
        (qubits, mat.tolist()),
        (mat, qubits),
        (mat.tolist(), qubits),
    )

    last_error = None
    for args in attempts:
        try:
            circuit = decompose_fn(*args)
            decompose_unitary._last_qvm = qvm
            return circuit
        except Exception as exc:
            last_error = exc

    raise last_error
