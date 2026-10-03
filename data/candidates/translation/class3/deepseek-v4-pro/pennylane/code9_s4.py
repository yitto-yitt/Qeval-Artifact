# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    return qml.EfficientSU2(wires=range(3), n_layers=1)
