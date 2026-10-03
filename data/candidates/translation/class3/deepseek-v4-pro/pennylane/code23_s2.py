# EVAL_META: task_id=23, framework=pennylane, class=3
import pennylane as qml

def dj_constant_oracle():
    dev = qml.device('default.qubit', wires=3)

    @qml.qnode(dev)
    def oracle():
        qml.PauliX(wires=2)
        return qml.state()

    return oracle
