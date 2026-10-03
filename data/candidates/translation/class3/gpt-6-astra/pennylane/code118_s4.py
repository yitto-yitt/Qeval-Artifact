# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    return qml.tape.QuantumScript(
        [qml.ctrl(qml.SX(wires=3), control=[0, 1, 2])]
    )
