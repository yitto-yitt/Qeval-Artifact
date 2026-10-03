# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml

def qft_no_swaps(num_qubits):
    def circuit():
        # Apply inverse QFT without swaps - implement manually
        for i in range(num_qubits):
            # Apply inverse Hadamard to the last qubit in the sequence
            qml.Hadamard(wires=num_qubits - 1 - i)
            
            # Apply controlled rotations
            for j in range(i):
                control_wire = num_qubits - 1 - j
                target_wire = num_qubits - 1 - i
                angle = -2 * 3.141592653589793 / (2 ** (i - j + 1))
                qml.ctrl(qml.RZ, control=control_wire)(angle, wires=target_wire)
    
    return circuit
