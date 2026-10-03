# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device('default.qubit', wires=3)

    @qml.qnode(dev)
    def circuit(params):
        qml.EfficientSU2(
            weights=params,
            wires=[0, 1, 2],
            reps=1,
            entanglement='full',
            insert_barriers=True,
        )
        return qml.state()

    return circuit
