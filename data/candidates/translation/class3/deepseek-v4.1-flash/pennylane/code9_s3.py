# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(weights):
        qml.EfficientSU2(weights, wires=[0, 1, 2], reps=1, insert_barriers=True)
    return circuit
