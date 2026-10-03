# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        def qft_rotations(k):
            if k == 0:
                return
            k -= 1
            qml.Hadamard(wires=k)
            for qubit in range(k):
                qml.ControlledPhaseShift(pi / 2 ** (k - qubit), wires=[qubit, k])
            qft_rotations(k)

        qft_rotations(n)

        for qubit in range(n // 2):
            qml.SWAP(wires=[qubit, n - qubit - 1])

        return qml.state()

    return circuit
