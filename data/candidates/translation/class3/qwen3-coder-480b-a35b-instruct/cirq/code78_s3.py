# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Apply inverse QFT without swaps - reverse order of operations compared to forward QFT
    for i in range(num_qubits):
        # Apply inverse Hadamard (which is just Hadamard since H^2 = I)
        circuit.append(cirq.H(qubits[num_qubits - 1 - i]))
        
        # Apply controlled phase rotations
        for j in range(i + 1, num_qubits):
            angle = -np.pi / (2 ** (j - i))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[num_qubits - 1 - j], qubits[num_qubits - 1 - i]))
    
    return circuit
