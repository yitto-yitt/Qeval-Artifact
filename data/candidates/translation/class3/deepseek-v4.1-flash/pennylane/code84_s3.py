# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    dev = qml.device("default.qubit", wires=2)

    theta = 0.3
    phi = 0.2
    lam = 0.1
    U = np.array([
        [np.cos(theta / 2), -np.exp(1j * lam) * np.sin(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]
    ])

    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.QubitUnitary(U, wires=1), control=0)
        return qml.state()

    return circuit
