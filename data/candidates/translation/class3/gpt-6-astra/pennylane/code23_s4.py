# EVAL_META: task_id=23, framework=pennylane, class=3
import pennylane as qml

def dj_constant_oracle():
    return qml.tape.QuantumScript(
        [
            qml.Identity(wires=0),
            qml.Identity(wires=1),
            qml.PauliX(wires=2),
        ]
    )
