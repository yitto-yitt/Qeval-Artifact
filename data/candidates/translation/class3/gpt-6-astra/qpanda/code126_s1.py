# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    gate = pq.H(0)
    circuit = pq.QCircuit()
    circuit << gate

    op_a = None
    for obj in (gate, circuit):
        for name in ("matrix", "get_matrix", "getMatrix", "get_unitary"):
            accessor = getattr(obj, name, None)
            if accessor is None:
                continue
            try:
                matrix = accessor() if callable(accessor) else accessor
                op_a = np.asarray(matrix, dtype=complex).reshape(2, 2)
                break
            except (TypeError, ValueError, RuntimeError):
                continue
        if op_a is not None:
            break

    if op_a is None:
        for name in ("get_matrix", "get_unitary", "get_circuit_matrix"):
            accessor = getattr(pq, name, None)
            if not callable(accessor):
                continue
            try:
                op_a = np.asarray(accessor(circuit), dtype=complex).reshape(2, 2)
                break
            except (TypeError, ValueError, RuntimeError):
                continue

    if op_a is None:
        raise RuntimeError("Unable to obtain the Hadamard operator from pyQPanda3.")

    op_b = np.exp(1j * 0.5) * op_a
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / 4
    return float(fidelity)
