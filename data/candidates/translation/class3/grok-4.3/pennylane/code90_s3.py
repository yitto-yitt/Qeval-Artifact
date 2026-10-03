# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    with qml.tape.QuantumTape() as tape:
        qml.ctrl(qml.PauliX, control=[0, 3])(wires=1)
        qml.ctrl(qml.Hadamard, control=[0, 3])(wires=2)
    return tape
