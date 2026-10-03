# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(weights):
        for i in range(3):
            qml.RY(weights[2 * i], wires=i)
            qml.RZ(weights[2 * i + 1], wires=i)
        qml.Barrier(wires=range(3))
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        qml.CNOT(wires=[1, 2])
    return circuit
