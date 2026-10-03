# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def create_operator():
    target = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [1, 0, 0, 0]], dtype=complex)

    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(target, wires=[0, 1])
        return qml.state()

    decomposed = qml.transforms.decompose(
        circuit, gate_set={"RZ", "RY", "CNOT", "PauliX", "PauliZ", "Hadamard"}
    )
    return decomposed
