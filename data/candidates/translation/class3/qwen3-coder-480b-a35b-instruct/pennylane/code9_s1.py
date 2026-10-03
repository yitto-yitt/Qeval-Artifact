# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(params):
        qml.layer(lambda p, w: [qml.RY(p[0], wires=w), qml.RZ(p[1], wires=w)], 1, [[0, 1, 2]])
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.RY(params[2], wires=0)
        qml.RZ(params[3], wires=0)
        qml.RY(params[4], wires=1)
        qml.RZ(params[5], wires=1)
        qml.RY(params[6], wires=2)
        qml.RZ(params[7], wires=2)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        
    return circuit
