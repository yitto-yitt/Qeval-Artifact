# EVAL_META: task_id=13, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def custom_rotation_gate():
    dev = qml.device("default.qubit", wires=1)
    @qml.qnode(dev)
    def circuit():
        matrix = np.array([[1, -1j], [1j, -1]]) / np.sqrt(2)
        qml.QubitUnitary(matrix, wires=0)
        return qml.state()
    return circuit
