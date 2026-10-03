# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml
from math import pi

def qft_inverse(n):
    with qml.tape.QuantumTape() as circuit:
        for j in range(n // 2):
            qml.SWAP(wires=[j, n - j - 1])
        for j in range(n):
            for k in range(j):
                qml.ControlledPhaseShift(-pi / (2 ** (j - k)), wires=[j, k])
            qml.Hadamard(wires=j)
    return circuit
