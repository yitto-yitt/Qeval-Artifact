# EVAL_META: task_id=23, framework=pennylane, class=3
import pennylane as qml

def dj_constant_oracle():
    with qml.tape.QuantumTape() as tape:
        qml.Identity(0)
        qml.Identity(1)
        qml.X(2)
    return tape
