# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def create_c3sx_circuit():
    qml.ctrl(qml.SX(wires=3), control=[0, 1, 2])
    return qml.state()
