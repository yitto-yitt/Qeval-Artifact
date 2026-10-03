# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml


def qft_inverse(n):
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.adjoint(qml.QFT)(wires=range(n))
        return qml.state()

    return circuit
