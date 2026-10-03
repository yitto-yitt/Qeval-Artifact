# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    with qml.tape.QuantumTape() as tape:
        def custom_gate(wires):
            qml.PauliX(wires=wires[0])
            qml.Hadamard(wires=wires[1])
        qml.ctrl(custom_gate, control=[0, 3])(wires=[1, 2])
    return tape
