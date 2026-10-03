# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    diag_arr = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag_arr)))
    if 2**n != len(diag_arr):
        raise ValueError("Length of diag must be a power of 2.")
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(np.diag(diag_arr)).on(*qubits))
    return circuit
