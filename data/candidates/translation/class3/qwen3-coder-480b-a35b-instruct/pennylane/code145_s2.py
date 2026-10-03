# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml

def qft_inverse(n):
    def circuit():
        # Apply inverse QFT by applying gates in reverse order with conjugate angles
        for i in range(n):
            # Apply Hadamard to the current qubit
            qml.Hadamard(wires=n-1-i)
            
            # Apply controlled phase shift gates in reverse order
            for j in range(i):
                angle = -2 * 3.141592653589793 / (2 ** (i - j + 1))
                qml.CRot(0, 0, angle, wires=[n-1-(i-j), n-1-i])
        
        # Reverse the order of qubits at the end
        for i in range(n // 2):
            qml.SWAP(wires=[i, n-1-i])
    
    return circuit
