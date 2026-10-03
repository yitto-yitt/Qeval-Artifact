# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    def circuit():
        def qft_rotations(m):
            if m == 0:
                return
            m -= 1
            qml.Hadamard(wires=m)
            for qubit in range(m):
                qml.ControlledPhaseShift(pi / (2 ** (m - qubit)), wires=[qubit, m])
            qft_rotations(m)
        
        qft_rotations(n)
        for qubit in range(n // 2):
            qml.SWAP(wires=[qubit, n - qubit - 1])
            
    return circuit
