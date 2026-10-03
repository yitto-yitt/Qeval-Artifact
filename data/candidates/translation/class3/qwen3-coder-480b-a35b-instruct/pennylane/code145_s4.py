# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml

def qft_inverse(n):
    def circuit():
        for i in range(n):
            qml.Hadamard(wires=n-1-i)
            for j in range(i):
                qml.ControlledPhase(-qml.math.pi / 2**(i-j), wires=[n-1-i, n-1-j])
    
    return circuit
