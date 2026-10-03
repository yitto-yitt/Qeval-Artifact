# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            theta = -np.pi / (2 ** (j - i))
            circuit.append((cirq.CZ ** (theta / np.pi)).on(qubits[j], qubits[i]))
        circuit.append(cirq.H(qubits[i]))
    return circuit
