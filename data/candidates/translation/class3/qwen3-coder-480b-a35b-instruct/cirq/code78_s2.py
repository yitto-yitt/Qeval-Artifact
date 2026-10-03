# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Apply inverse QFT without swaps (reversed order compared to forward QFT)
    for i in range(num_qubits):
        # Apply inverse Hadamard (which is just Hadamard since H^2 = I)
        circuit.append(cirq.H(qubits[i]))
        
        # Apply inverse controlled rotations
        for j in range(i + 1, num_qubits):
            angle = -np.pi / (2 ** (j - i))
            circuit.append(cirq.Rz(angle).controlled_by(qubits[j])(qubits[i]))
    
    return circuit
