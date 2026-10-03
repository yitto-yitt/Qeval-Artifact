# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    dev = qml.device('default.qubit', wires=n)

    @qml.qnode(dev)
    def circuit():
        for top in range(n - 1, -1, -1):
            qml.Hadamard(wires=top)
            for qubit in range(top):
                qml.ControlledPhaseShift(
                    phi=pi / 2 ** (top - qubit),
                    wires=[qubit, top]
                )

        for qubit in range(n // 2):
            qml.SWAP(wires=[qubit, n - qubit - 1])

        return qml.state()

    return circuit
