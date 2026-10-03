# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    with qml.tape.QuantumTape() as tape:
        for k in range(n-1, -1, -1):
            qml.Hadamard(wires=k)
            for j in range(k):
                qml.ControlledPhaseShift(pi / (2 ** (k - j)), wires=[j, k])
        for i in range(n // 2):
            qml.SWAP(wires=[i, n - i - 1])
    return tape
