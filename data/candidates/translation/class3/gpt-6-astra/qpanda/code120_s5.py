# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, X, U1


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1 or diagonal.size < 2:
        raise ValueError("diag must contain at least two diagonal entries.")
    size = diagonal.size
    if size & (size - 1):
        raise ValueError("The number of diagonal entries must be a power of two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("Every diagonal entry must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    controls = list(range(1, num_qubits))
    program = QProg()

    for basis_state, value in enumerate(diagonal):
        flipped = [
            qubit
            for qubit in range(num_qubits)
            if not (basis_state & (1 << qubit))
        ]
        for qubit in flipped:
            program << X(qubit)

        phase_gate = U1(0, float(np.angle(value)))
        if controls:
            phase_gate = phase_gate.control(controls)
        program << phase_gate

        for qubit in reversed(flipped):
            program << X(qubit)

    return program
