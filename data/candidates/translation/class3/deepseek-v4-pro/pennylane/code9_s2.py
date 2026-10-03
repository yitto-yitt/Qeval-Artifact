# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device('default.qubit', wires=3)

    @qml.qnode(dev)
    def circuit(params):
        # First rotation layer
        qml.RY(params[0], wires=0)
        qml.RY(params[1], wires=1)
        qml.RY(params[2], wires=2)
        qml.RZ(params[3], wires=0)
        qml.RZ(params[4], wires=1)
        qml.RZ(params[5], wires=2)
        qml.Barrier(wires=[0, 1, 2])

        # Entanglement layer
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        qml.CNOT(wires=[1, 2])
        qml.Barrier(wires=[0, 1, 2])

        # Final rotation layer
        qml.RY(params[6], wires=0)
        qml.RY(params[7], wires=1)
        qml.RY(params[8], wires=2)
        qml.RZ(params[9], wires=0)
        qml.RZ(params[10], wires=1)
        qml.RZ(params[11], wires=2)
        qml.Barrier(wires=[0, 1, 2])

        return qml.state()

    return circuit
