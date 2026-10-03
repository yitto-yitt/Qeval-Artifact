# EVAL_META: task_id=125, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def circ_to_gate(circ):
    to_gate = getattr(circ, "to_gate", None)
    if callable(to_gate):
        return to_gate()

    qubits = None
    for name in ("get_used_qubits", "get_qubits", "get_all_used_qubits"):
        getter = getattr(circ, name, None)
        if callable(getter):
            qubits = list(getter())
            break
    if qubits is None:
        getter = getattr(pq, "get_all_used_qubits", None)
        if callable(getter):
            qubits = list(getter(circ))
    if qubits is None:
        raise TypeError("Cannot determine the circuit's qubits.")

    matrix = None
    for name in ("get_matrix", "get_unitary"):
        getter = getattr(pq, name, None)
        if callable(getter):
            matrix = getter(circ)
            break
        getter = getattr(circ, name, None)
        if callable(getter):
            matrix = getter()
            break
    if matrix is None:
        raise TypeError("The circuit does not expose a unitary matrix.")

    dimension = 1 << len(qubits)
    matrix = np.asarray(matrix, dtype=complex).reshape(dimension, dimension)

    for name in ("QOracle", "Oracle"):
        constructor = getattr(pq, name, None)
        if callable(constructor):
            try:
                return constructor(qubits, matrix)
            except TypeError:
                return constructor(qubits, matrix.ravel().tolist())

    raise TypeError("The framework does not expose a matrix-defined gate.")
