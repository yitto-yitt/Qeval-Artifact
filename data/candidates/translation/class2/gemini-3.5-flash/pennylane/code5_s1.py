# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def create_state_prep():
    qml.PauliX(wires=1)
    return qml.state()
