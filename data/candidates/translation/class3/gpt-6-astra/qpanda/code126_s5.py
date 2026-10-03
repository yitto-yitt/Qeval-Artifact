# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    gate = pq.H(0)
    op_a = None

    for name in ("matrix", "get_matrix", "gate_matrix"):
        accessor = getattr(gate, name, None)
        if accessor is not None:
            matrix = accessor() if callable(accessor) else accessor
            op_a = np.asarray(matrix, dtype=complex).reshape(2, 2)
            break

    if op_a is None:
        program = pq.QProg()
        program << gate
        op_a = np.asarray(pq.get_matrix(program), dtype=complex).reshape(2, 2)

    op_b = np.exp(0.5j) * op_a
    overlap = np.trace(op_a.conj().T @ op_b)
    return float(np.abs(overlap) ** 2 / 4.0)
