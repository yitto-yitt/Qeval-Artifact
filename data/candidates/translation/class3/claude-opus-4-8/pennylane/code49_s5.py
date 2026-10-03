# EVAL_META: task_id=49, framework=pennylane, class=3
import pennylane as qml

def simple_elitzur_vaidman():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        return qml.state()

    return circuit
