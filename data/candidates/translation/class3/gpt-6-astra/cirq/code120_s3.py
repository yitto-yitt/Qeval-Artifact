# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np


def create_diagonal_circuit(diag):
    values = np.asarray(diag, dtype=complex)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("diag must be a nonempty one-dimensional sequence.")
    size = values.size
    if size & (size - 1):
        raise ValueError("The number of diagonal elements must be a power of two.")
    if not np.allclose(np.abs(values), 1.0):
        raise ValueError("All diagonal elements must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(np.diag(values))
    return cirq.Circuit(gate.on(*reversed(qubits)))
