# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    tape = qml.tape.QuantumTape()
    with tape:
        qml.SX(wires=3).controlled(control_wires=[0, 1, 2])
    return tape
