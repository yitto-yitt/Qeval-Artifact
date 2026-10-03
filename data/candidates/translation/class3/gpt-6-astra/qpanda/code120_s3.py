# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, U1, X


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1:
        raise ValueError("diag must be a one-dimensional sequence.")

    size = len(diagonal)
    if size < 2 or size & (size - 1):
        raise ValueError("diag must have power-of-two length of at least two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("Every diagonal element must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    controls = list(range(1, num_qubits))
    program = QProg()

    for basis_index, element in enumerate(diagonal):
        flipped = [
            qubit
            for qubit in range(num_qubits)
            if not ((basis_index >> qubit) & 1)
        ]

        for qubit in flipped:
            program << X(qubit)

        phase_gate = U1(0, float(np.angle(element)))
        if controls:
            phase_gate = phase_gate.control(controls)
        program << phase_gate

        for qubit in reversed(flipped):
            program << X(qubit)

    return program
