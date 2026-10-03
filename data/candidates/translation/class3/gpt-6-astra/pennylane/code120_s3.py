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
        raise ValueError("Diagonal elements must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    with qml.tape.QuantumTape() as circuit:
        if num_qubits:
            qml.DiagonalQubitUnitary(diagonal, wires=range(num_qubits))
        else:
            qml.GlobalPhase(-np.angle(diagonal[0]))
    return circuit
