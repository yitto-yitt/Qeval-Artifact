# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    with qml.tape.QuantumTape() as tape:
        qml.ctrl(qml.SX(3), control=[0, 1, 2])
    return tape
