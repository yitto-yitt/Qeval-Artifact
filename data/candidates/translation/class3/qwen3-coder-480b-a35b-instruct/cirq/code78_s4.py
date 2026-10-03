# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Apply inverse QFT without swaps - reverse the order of operations compared to normal QFT
    for i in range(num_qubits):
        # Apply Hadamard gate
        circuit.append(cirq.H(qubits[i]))
        
        # Apply controlled phase gates
        for j in range(i + 1, num_qubits):
            angle = -2 * np.pi / (2 ** (j - i + 1))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[j], qubits[i]))
    
    return circuit
