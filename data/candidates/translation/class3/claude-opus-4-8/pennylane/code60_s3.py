# EVAL_META: task_id=60, framework=pennylane, class=3
import pennylane as qml

def create_cy_gate():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.adjoint(qml.S(wires=1))
        qml.CNOT(wires=[0, 1])
        qml.S(wires=1)
        return qml.state()

    return circuit
