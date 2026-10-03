# EVAL_META: task_id=39, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def create_uniform_superposition(n):
    if n == 0:
        return np.array([1.0 + 0.0j])
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for wire in range(n):
            qml.Hadamard(wires=wire)
        return qml.state()

    return circuit()
