# EVAL_META: task_id=125, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def circ_to_gate(circ):
    for name in ("to_gate", "as_gate"):
        convert = getattr(circ, name, None)
        if callable(convert):
            return convert()

    convert = getattr(pq, "circuit_to_gate", None)
    if callable(convert):
        return convert(circ)

    qubits = None
    for name in ("get_used_qubits", "get_qubits", "qubits", "used_qubits"):
        value = getattr(circ, name, None)
        if value is not None:
            try:
                qubits = list(value() if callable(value) else value)
                break
            except (TypeError, ValueError):
                pass

    if qubits is None:
        for name in ("get_used_qubits", "get_qubits"):
            getter = getattr(pq, name, None)
            if callable(getter):
                try:
                    qubits = list(getter(circ))
                    break
                except (TypeError, ValueError):
                    pass

    representations = [circ]
    for name in ("QCircuit", "QProg"):
        cls = getattr(pq, name, None)
        if cls is not None and not isinstance(circ, cls):
            try:
                wrapped = cls()
                wrapped << circ
                representations.append(wrapped)
            except (TypeError, ValueError, RuntimeError):
                pass

    matrix = None
    for obj in representations:
        for name in ("get_matrix", "get_unitary", "to_matrix", "matrix"):
            getter = getattr(obj, name, None)
            if getter is not None:
                try:
                    value = getter() if callable(getter) else getter
                    matrix = np.asarray(value, dtype=complex)
                    break
                except (TypeError, ValueError, RuntimeError):
                    pass
        if matrix is not None:
            break

        for name in ("get_matrix", "get_unitary", "circuit_to_matrix"):
            getter = getattr(pq, name, None)
            if callable(getter):
                try:
                    matrix = np.asarray(getter(obj), dtype=complex)
                    break
                except (TypeError, ValueError, RuntimeError):
                    pass
        if matrix is not None:
            break

    if matrix is None:
        raise TypeError("The input does not expose a unitary matrix through pyQPanda3.")

    if matrix.ndim == 1:
        dimension = int(np.sqrt(matrix.size))
        matrix = matrix.reshape(dimension, dimension)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("The circuit matrix must be square.")

    dimension = matrix.shape[0]
    if dimension == 0 or dimension & (dimension - 1):
        raise ValueError("The circuit matrix dimension must be a power of two.")

    if qubits is None:
        qubits = list(range(dimension.bit_length() - 1))

    last_error = None
    for name in ("QOracle", "Oracle", "U_matrix", "QGate"):
        factory = getattr(pq, name, None)
        if not callable(factory):
            continue
        for data in (matrix, matrix.tolist(), matrix.ravel().tolist()):
            for args in ((qubits, data), (data, qubits)):
                try:
                    return factory(*args)
                except (TypeError, ValueError, RuntimeError) as error:
                    last_error = error

    raise TypeError("Unable to construct a pyQPanda3 matrix gate.") from last_error
