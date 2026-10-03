# EVAL_META: task_id=145, framework=pennylane, class=3
import math
import pennylane as qml

def qft_inverse(n):
    operations = []
    for i in range(n // 2):
        operations.append(qml.SWAP(wires=[i, n - i - 1]))
    for j in range(n):
        for k in range(j):
            operations.append(
                qml.ControlledPhaseShift(-math.pi / (2 ** (j - k)), wires=[j, k])
            )
        operations.append(qml.Hadamard(wires=j))
    return qml.tape.QuantumScript(operations)
