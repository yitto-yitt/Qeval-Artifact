# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Apply inverse QFT without swaps
    for i in range(num_qubits):
        # Apply Hadamard gate
        circuit.append(cirq.H(qubits[i]))
        
        # Apply controlled phase gates in reverse order for inverse QFT
        for j in range(i + 1, num_qubits):
            angle = -np.pi / (2 ** (j - i))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[j], qubits[i]))
    
    return circuit
