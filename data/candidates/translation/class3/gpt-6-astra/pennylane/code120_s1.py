# EVAL_META: task_id=120, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1 or diagonal.size == 0:
        raise ValueError("diag must be a nonempty one-dimensional sequence.")

    size = diagonal.size
    if size & (size - 1):
        raise ValueError("The number of diagonal elements must be a power of two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("Each diagonal element must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    operation = qml.DiagonalQubitUnitary(
        diagonal, wires=list(reversed(range(num_qubits)))
    )
    return qml.tape.QuantumScript([operation])
