# EVAL_META: task_id=23, framework=pennylane, class=3
import pennylane as qml

def dj_constant_oracle():
    def circuit():
        qml.PauliX(wires=2)
    return circuit
