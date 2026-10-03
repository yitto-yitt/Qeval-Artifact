# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    diag_array = np.asarray(diag, dtype=complex)
    num_qubits = int(np.log2(len(diag_array)))
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    if num_qubits > 0:
        circuit.append(cirq.MatrixGate(np.diag(diag_array)).on(*qubits))
    return circuit
