# EVAL_META: task_id=109, framework=pennylane, class=3
import pennylane as qml

def circuit():
    theta = qml.numpy.array(0.0, requires_grad=True)

    @qml.qnode(qml.device("default.qubit", wires=1))
    def qnode(th):
        qml.Hadamard(wires=0)
        qml.RZ(th, wires=0)
        return qml.state()

    return qnode
