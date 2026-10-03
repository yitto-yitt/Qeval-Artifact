# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml

def qft_no_swaps(num_qubits):
    def circuit():
        # Apply inverse QFT without swaps - reverse the order of operations compared to forward QFT
        for i in range(num_qubits):
            qml.Hadamard(wires=i)
            for j in range(1, num_qubits - i):
                angle = -2 * qml.math.pi / (2 ** (j + 1))
                qml.ctrl(qml.RZ(angle), control=i + j, wires=i)
    
    return circuit
