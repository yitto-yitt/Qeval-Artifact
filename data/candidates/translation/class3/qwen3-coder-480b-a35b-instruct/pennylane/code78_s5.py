# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml

def qft_no_swaps(num_qubits):
    def circuit():
        # Apply inverse QFT without swaps - reverse the order of operations compared to forward QFT
        for i in range(num_qubits):
            qml.Hadamard(wires=i)
            for j in range(i + 1, num_qubits):
                # Apply controlled phase rotations
                angle = -2 * 3.141592653589793 / (2 ** (j - i + 1))
                qml.CRot(0, 0, angle, wires=[j, i])
    
    return circuit
