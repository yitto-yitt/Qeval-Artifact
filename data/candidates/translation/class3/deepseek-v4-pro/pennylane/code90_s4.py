# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_custom_controlled():
    X = np.array([[0, 1], [1, 0]])
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    U = np.kron(H, X)

    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def circuit():
        qml.ControlledQubitUnitary(U, control_wires=[0, 3], wires=[1, 2])
        return qml.state()

    return circuit
