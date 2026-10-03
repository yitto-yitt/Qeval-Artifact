# EVAL_META: task_id=145, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def qft_inverse(n):
    ops = []
    for i in range(n // 2):
        ops.append(qml.SWAP(wires=[i, n - i - 1]))
    for i in range(n - 1, -1, -1):
        for j in range(n - i, 1, -1):
            ops.append(qml.ControlledPhaseShift(-2 * np.pi / (2 ** j),
                                                wires=[i + j - 1, i]))
        ops.append(qml.Hadamard(wires=i))
    return qml.tape.QuantumScript(ops)
