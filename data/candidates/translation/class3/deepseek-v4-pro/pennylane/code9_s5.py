# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        weights = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]], requires_grad=True)

        # First rotation layer: RY on all qubits
        for i in range(3):
            qml.RY(weights[0][i], wires=i)

        qml.Barrier(wires=[0, 1, 2])

        # Second rotation layer: RZ on all qubits
        for i in range(3):
            qml.RZ(weights[0][i + 3], wires=i)

        qml.Barrier(wires=[0, 1, 2])

        # Entanglement layer: full entanglement
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        qml.CNOT(wires=[1, 2])

        qml.Barrier(wires=[0, 1, 2])

        return qml.state()

    return circuit
