# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    dev = qml.device("default.qubit", wires=n)
    
    def qft_rotations(n):
        if n == 0:
            return
        n -= 1
        qml.Hadamard(wires=n)
        for qubit in range(n):
            qml.ControlledPhaseShift(pi / 2**(n - qubit), wires=[qubit, n])
        qft_rotations(n)
    
    @qml.qnode(dev)
    def circuit():
        qft_rotations(n)
        for qubit in range(n // 2):
            qml.SWAP(wires=[qubit, n - qubit - 1])
        return qml.state()
    
    return circuit
