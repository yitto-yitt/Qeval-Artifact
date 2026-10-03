# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml


def tensor_circuits():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        # top (1-qubit X circuit) placed on lower qubit index
        qml.PauliX(wires=0)
        # bottom (2-qubit CRY circuit) placed on higher qubit indices
        qml.CRY(0.2, wires=[1, 2])
        return qml.state()

    return circuit
