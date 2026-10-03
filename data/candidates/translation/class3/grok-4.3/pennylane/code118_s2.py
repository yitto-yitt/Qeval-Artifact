# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    op = qml.ctrl(qml.SX, control=[0, 1, 2])(wires=3)
    return qml.tape.QuantumScript([op], [])
