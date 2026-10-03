# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    diag_arr = np.asarray(diag, dtype=complex)
    if diag_arr.ndim != 1 or diag_arr.size == 0 or (diag_arr.size & (diag_arr.size - 1)) != 0:
        raise ValueError("diag must be a non-empty 1D sequence with length a power of 2.")
    num_qubits = int(np.log2(diag_arr.size))
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.DiagonalGate(diag_arr)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
