# EVAL_META: task_id=125, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def circ_to_gate(circ):
    for name in ("to_gate", "to_qgate"):
        converter = getattr(circ, name, None)
        if callable(converter):
            return converter()

    converter = getattr(pq, "circuit_to_gate", None)
    if callable(converter):
        return converter(circ)

    program = pq.QProg()
    program << circ

    matrix = None
    for obj in (circ, program):
        for name in ("get_matrix", "get_unitary", "matrix"):
            getter = getattr(obj, name, None)
            if getter is not None:
                try:
                    matrix = getter() if callable(getter) else getter
                except (TypeError, ValueError, RuntimeError):
                    continue
                if matrix is not None:
                    break
        if matrix is not None:
            break

    if matrix is None:
        for name in ("get_matrix", "get_circuit_matrix", "get_unitary"):
            getter = getattr(pq, name, None)
            if not callable(getter):
                continue
            for obj in (program, circ):
                try:
                    matrix = getter(obj)
                except (TypeError, ValueError, RuntimeError):
                    continue
                if matrix is not None:
                    break
            if matrix is not None:
                break

    if matrix is None:
        raise TypeError("The input circuit does not expose a unitary matrix.")

    matrix = np.asarray(matrix, dtype=complex)
    if matrix.ndim == 1:
        dimension = int(round(np.sqrt(matrix.size)))
        matrix = matrix.reshape(dimension, dimension)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("The circuit matrix must be square.")

    dimension = matrix.shape[0]
    width = dimension.bit_length() - 1
    if dimension != 1 << width:
        raise ValueError("The circuit matrix dimension must be a power of two.")

    qubits = None
    for obj in (circ, program):
        for name in ("get_used_qubits", "get_qubits", "qubits", "used_qubits"):
            getter = getattr(obj, name, None)
            if getter is None:
                continue
            try:
                value = getter() if callable(getter) else getter
                candidate = sorted(value)
            except (TypeError, ValueError, RuntimeError):
                continue
            if len(candidate) == width:
                qubits = candidate
                break
        if qubits is not None:
            break

    if qubits is None:
        getter = getattr(pq, "get_all_used_qubits", None)
        if callable(getter):
            try:
                candidate = sorted(getter(program))
                if len(candidate) == width:
                    qubits = candidate
            except (TypeError, ValueError, RuntimeError):
                pass

    if qubits is None:
        qubits = list(range(width))

    last_error = None
    for name in ("QOracle", "Uany"):
        constructor = getattr(pq, name, None)
        if not callable(constructor):
            continue
        for data in (matrix, matrix.tolist(), matrix.ravel().tolist()):
            try:
                return constructor(qubits, data)
            except (TypeError, ValueError, RuntimeError) as error:
                last_error = error

    if last_error is not None:
        raise last_error
    raise TypeError("No arbitrary-unitary gate constructor is available.")
