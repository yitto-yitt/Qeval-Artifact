# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    with qml.tape.QuantumTape() as tape:
        qml.ctrl(qml.PauliX(wires=1), control=[0, 3])
        qml.ctrl(qml.Hadamard(wires=2), control=[0, 3])
    return tape
