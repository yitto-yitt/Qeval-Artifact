# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=np.complex128)
    if diagonal.ndim != 1 or diagonal.size == 0:
        raise ValueError("diag must be a nonempty one-dimensional sequence.")
    if diagonal.size & (diagonal.size - 1):
        raise ValueError("The number of diagonal elements must be a power of two.")
    num_qubits = diagonal.size.bit_length() - 1
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(np.diag(diagonal))
    return cirq.Circuit(gate.on(*reversed(qubits)))
