# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_operator():
    XX = np.array([[0, 0, 0, 1],
                   [0, 0, 1, 0],
                   [0, 1, 0, 0],
                   [1, 0, 0, 0]], dtype=complex)

    @qml.transforms.compile(basis_set=["RX", "RY", "RZ", "CNOT"], num_passes=1)
    @qml.qnode(qml.device("default.qubit", wires=2))
    def circuit():
        qml.QubitUnitary(XX, wires=[0, 1])
        return qml.state()

    return circuit
