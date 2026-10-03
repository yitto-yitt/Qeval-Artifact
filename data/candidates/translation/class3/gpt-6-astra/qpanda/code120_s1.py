# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, X, U1


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1:
        raise ValueError("diag must be a one-dimensional sequence.")
    size = len(diagonal)
    if size < 2 or size & (size - 1):
        raise ValueError("The diagonal length must be a power of two, at least two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("Every diagonal entry must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    target = num_qubits - 1
    controls = list(range(target))
    program = QProg()

    for basis_state, entry in enumerate(diagonal):
        inverted = [
            qubit
            for qubit in range(num_qubits)
            if not (basis_state & (1 << qubit))
        ]
        for qubit in inverted:
            program << X(qubit)

        phase_gate = U1(target, float(np.angle(entry)))
        if controls:
            phase_gate = phase_gate.control(controls)
        program << phase_gate

        for qubit in reversed(inverted):
            program << X(qubit)

    return program
