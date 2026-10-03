# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1 or diagonal.size == 0:
        raise ValueError("diag must be a nonempty one-dimensional sequence.")
    size = diagonal.size
    if size & (size - 1):
        raise ValueError("The number of diagonal entries must be a power of two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("All diagonal entries must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.DiagonalGate(tuple(np.angle(diagonal)))
    return cirq.Circuit(gate.on(*reversed(qubits)))
