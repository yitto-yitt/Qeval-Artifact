# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit(params):
        # First SU(2) layer (RY + RZ on each qubit)
        for i in range(3):
            qml.RY(params[2 * i], wires=i)
            qml.RZ(params[2 * i + 1], wires=i)

        qml.Barrier(wires=[0, 1, 2])

        # Entangling layer (reverse_linear CNOTs)
        qml.CNOT(wires=[2, 1])
        qml.CNOT(wires=[1, 0])

        qml.Barrier(wires=[0, 1, 2])

        # Second SU(2) layer (reps=1)
        for i in range(3):
            qml.RY(params[6 + 2 * i], wires=i)
            qml.RZ(params[6 + 2 * i + 1], wires=i)

        return qml.state()

    return circuit
