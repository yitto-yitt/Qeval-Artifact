# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_inverse(n):
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        wires = list(range(n))
        for i in range(n // 2):
            qml.SWAP(wires=[wires[i], wires[n - 1 - i]])
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                qml.ControlledPhaseShift(-np.pi / 2**(j - i), wires=[wires[i], wires[j]])
            qml.Hadamard(wires=wires[i])
        return qml.state()
    return circuit
