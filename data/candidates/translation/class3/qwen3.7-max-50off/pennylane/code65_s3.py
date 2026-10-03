# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    with qml.tape.QuantumTape() as tape:
        for i in range(n - 1, -1, -1):
            qml.Hadamard(wires=i)
            for j in range(i):
                qml.ControlledPhaseShift(pi / (2**(i - j)), wires=[j, i])
        for i in range(n // 2):
            qml.SWAP(wires=[i, n - i - 1])
    return tape
