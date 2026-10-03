# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_c3sx_circuit():
    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def circuit():
        sx = np.array([[0.5 + 0.5j, 0.5 - 0.5j],
                       [0.5 - 0.5j, 0.5 + 0.5j]])
        qml.ControlledQubitUnitary(sx, control_wires=[0, 1, 2], wires=3)
        return qml.state()

    return circuit
