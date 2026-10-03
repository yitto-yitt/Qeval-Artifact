# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    gate = pq.H(0)
    circuit = pq.QCircuit()
    circuit << gate

    op_a = None
    for obj in (gate, circuit):
        for name in ("get_matrix", "matrix", "getMatrix", "get_unitary"):
            accessor = getattr(obj, name, None)
            if accessor is None:
                continue
            try:
                value = accessor() if callable(accessor) else accessor
                matrix = np.asarray(value, dtype=complex)
                if matrix.size == 4:
                    op_a = matrix.reshape(2, 2)
                    break
            except (TypeError, ValueError, RuntimeError):
                continue
        if op_a is not None:
            break

    if op_a is None:
        for name in ("get_matrix", "get_unitary"):
            accessor = getattr(pq, name, None)
            if accessor is None:
                continue
            try:
                matrix = np.asarray(accessor(circuit), dtype=complex)
                if matrix.size == 4:
                    op_a = matrix.reshape(2, 2)
                    break
            except (TypeError, ValueError, RuntimeError):
                continue

    if op_a is None:
        raise RuntimeError("Unable to extract the Hadamard operator from pyQPanda3.")

    op_b = np.exp(1j * 0.5) * op_a
    return float(np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / 4.0)
