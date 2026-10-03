# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Apply inverse QFT without swaps
    for i in range(num_qubits):
        circuit.append(cirq.H(qubits[i]))
        for j in range(i + 1, num_qubits):
            circuit.append(cirq.CZ(qubits[j], qubits[i]) ** (-1 / (2 ** (j - i))))
    
    # Reverse the order of qubits to match Qiskit's convention
    for i in range(num_qubits // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[num_qubits - 1 - i]))
    
    return circuit
