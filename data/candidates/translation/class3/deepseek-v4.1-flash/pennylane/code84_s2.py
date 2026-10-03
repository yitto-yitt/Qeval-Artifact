# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    U3 = np.array([
        [np.cos(theta/2), -np.exp(1j*lam)*np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lam))*np.cos(theta/2)]
    ])
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.QubitUnitary, control=0)(U3, wires=1)
        return qml.state()

    return circuit
