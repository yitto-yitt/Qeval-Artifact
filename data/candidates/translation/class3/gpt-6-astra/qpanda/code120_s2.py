# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, U1, X


def create_diagonal_circuit(diag):
    values = np.asarray(diag, dtype=complex)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("diag must be a nonempty one-dimensional sequence.")

    size = int(values.size)
    if size & (size - 1):
        raise ValueError("The length of diag must be a power of two.")
    if not np.allclose(np.abs(values), 1.0):
        raise ValueError("Every diagonal element must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    program = QProg()
    if num_qubits == 0:
        if not np.isclose(values[0], 1.0):
            raise ValueError("A nontrivial zero-qubit global phase is unsupported.")
        return program

    controls = list(range(1, num_qubits))
    for basis_index, value in enumerate(values):
        flipped = [
            qubit
            for qubit in range(num_qubits)
            if not (basis_index & (1 << qubit))
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
