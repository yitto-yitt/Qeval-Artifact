# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml
from math import pi

def qft_inverse(n):
    operations = []
    for j in range(n // 2):
        operations.append(qml.SWAP(wires=[j, n - j - 1]))
    for j in range(n):
        for k in range(j):
            operations.append(
                qml.ControlledPhaseShift(-pi / (2 ** (j - k)), wires=[j, k])
            )
        operations.append(qml.Hadamard(wires=j))
    return qml.tape.QuantumScript(operations)
