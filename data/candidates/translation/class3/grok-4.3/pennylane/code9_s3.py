# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    wires = 3
    reps = 1
    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit(weights):
        qml.EfficientSU2(weights, wires=range(wires))
        return qml.state()

    return circuit
