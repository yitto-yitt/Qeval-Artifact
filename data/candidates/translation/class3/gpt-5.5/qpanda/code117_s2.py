# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq
from pyqpanda3.core import *

def decompose_unitary(unitary):
    mat = np.asarray(getattr(unitary, "data", unitary), dtype=np.complex128).reshape((4, 4))

    qvm = pq.CPUQVM()
    for name in ("init_qvm", "init", "initialize"):
        init = getattr(qvm, name, None)
        if callable(init):
            try:
                init()
            except TypeError:
                pass
            break

    qubits = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        alloc = getattr(qvm, name, None)
        if callable(alloc):
            try:
                qubits = alloc(2)
                break
            except TypeError:
                pass

    if qubits is None:
        for pair in (("qAlloc",), ("qalloc",), ("allocate_qubit",)):
            alloc = getattr(qvm, pair[0], None)
            if callable(alloc):
                qubits = [alloc(), alloc()]
                break

    if qubits is None:
        raise RuntimeError("Unable to allocate qubits in pyQPanda3 CPUQVM.")

    if not hasattr(decompose_unitary, "_qvms"):
        decompose_unitary._qvms = []
    decompose_unitary._qvms.append(qvm)

    candidates = []
    for name in ("matrix_decompose", "MatrixDecompose", "unitary_decompose", "UnitaryDecompose"):
        func = globals().get(name, None)
        if callable(func) and func not in candidates:
            candidates.append(func)
        func = getattr(pq, name, None)
        if callable(func) and func not in candidates:
            candidates.append(func)

    last_exc = None
    for func in candidates:
        for args in (
            (qubits, mat),
            (qubits, np.matrix(mat)),
            (qubits, mat.tolist()),
            (mat, qubits),
            (np.matrix(mat), qubits),
            (mat.tolist(), qubits),
        ):
            try:
                return func(*args)
            except Exception as exc:
                last_exc = exc

    for name in ("QOracle", "OracleGate", "Unitary"):
        func = globals().get(name, None) or getattr(pq, name, None)
        if callable(func):
            for args in ((qubits, mat), (mat, qubits), (qubits, mat.tolist()), (mat.tolist(), qubits)):
                try:
                    gate = func(*args)
                    circ = pq.QCircuit()
                    if hasattr(circ, "insert"):
                        circ.insert(gate)
                    else:
                        circ << gate
                    return circ
                except Exception as exc:
                    last_exc = exc

    if last_exc is not None:
        raise last_exc
    raise RuntimeError("No suitable pyQPanda3 unitary decomposition API was found.")
