# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml


def inv_circuit(n):
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.CNOT(wires=[2, 4])
        qml.CNOT(wires=[1, 3])
        qml.Hadamard(wires=2)
        qml.Hadamard(wires=1)
        return qml.state()

    return circuit
