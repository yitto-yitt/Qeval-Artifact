# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, U1, X

def create_diagonal_circuit(diag):
    values = np.asarray(diag, dtype=complex)
    if values.ndim != 1:
        raise ValueError("diag must be a one-dimensional sequence.")
    size = len(values)
    if size < 2 or size & (size - 1):
        raise ValueError("The length of diag must be a power of two, at least two.")
    if not np.all(np.isfinite(values)) or not np.allclose(
        np.abs(values), 1.0, rtol=0.0, atol=1e-10
    ):
        raise ValueError("All diagonal entries must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    program = QProg()
    target = num_qubits - 1
    controls = list(range(target))

    for basis, value in enumerate(values):
        zero_bits = [
            qubit for qubit in range(num_qubits)
            if not (basis & (1 << qubit))
        ]
        for qubit in zero_bits:
            program << X(qubit)

        phase_gate = U1(target, float(np.angle(value)))
        if controls:
            phase_gate = phase_gate.control(controls)
        program << phase_gate

        for qubit in reversed(zero_bits):
            program << X(qubit)

    return program
