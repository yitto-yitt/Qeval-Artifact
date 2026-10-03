# EVAL_META: task_id=145, framework=pennylane, class=3
import math
import pennylane as qml

def qft_inverse(n):
    dev = qml.device('default.qubit', wires=n)

    @qml.qnode(dev)
    def circuit():
        # Inverse QFT reverses the original QFT:
        # first undo final swaps, then reverse the gate order.
        for i in range(n // 2):
            qml.SWAP(wires=[i, n - i - 1])

        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                qml.ControlledPhaseShift(
                    -math.pi / (2 ** (j - i)),
                    wires=[j, i]
                )
            qml.Hadamard(wires=i)

        return qml.state()

    return circuit
