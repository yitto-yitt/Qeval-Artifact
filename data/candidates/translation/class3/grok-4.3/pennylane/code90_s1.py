# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    tape = qml.tape.QuantumTape()
    with tape:
        qml.ctrl(qml.X(wires=1), control=[0, 3])
        qml.ctrl(qml.H(wires=2), control=[0, 3])
    return tape
