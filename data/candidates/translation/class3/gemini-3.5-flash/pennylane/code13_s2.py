# EVAL_META: task_id=13, framework=pennylane, class=3
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev)
def custom_rotation_gate():
    qml.U3(np.pi / 2, np.pi / 2, np.pi / 2, wires=0)
    return qml.state()
