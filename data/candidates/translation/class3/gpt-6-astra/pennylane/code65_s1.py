# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi


def QFT(n):
    with qml.tape.QuantumTape() as circuit:
        for target in range(n - 1, -1, -1):
            qml.Hadamard(wires=target)
            for control in range(target):
                qml.ControlledPhaseShift(
                    pi / 2 ** (target - control), wires=[control, target]
                )
        for qubit in range(n // 2):
            qml.SWAP(wires=[qubit, n - qubit - 1])
    return circuit
