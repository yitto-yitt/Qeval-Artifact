# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def ansatz(params):
        for q in range(3):
            qml.RY(params[0, q, 0], wires=q)
            qml.RZ(params[0, q, 1], wires=q)
        qml.Barrier(wires=range(3))
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.Barrier(wires=range(3))
        for q in range(3):
            qml.RY(params[1, q, 0], wires=q)
            qml.RZ(params[1, q, 1], wires=q)
        return qml.state()

    return ansatz
