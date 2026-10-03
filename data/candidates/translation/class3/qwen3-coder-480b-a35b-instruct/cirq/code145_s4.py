# EVAL_META: task_id=145, framework=cirq, class=3
import cirq
import numpy as np

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    # Apply inverse QFT operations
    for i in range(n):
        # Apply Hadamard gate to qubit i
        circuit.append(cirq.H(qubits[i]))
        
        # Apply controlled phase gates in reverse order
        for j in range(i + 1, n):
            angle = -np.pi / (2 ** (j - i))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[j], qubits[i]))
    
    # Reverse the order of qubits at the end
    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
    
    return circuit
