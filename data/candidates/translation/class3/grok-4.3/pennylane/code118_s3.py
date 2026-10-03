# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    c3sx_op = qml.ctrl(qml.SX(wires=3), control=[0, 1, 2])
    return qml.QuantumScript([c3sx_op])
