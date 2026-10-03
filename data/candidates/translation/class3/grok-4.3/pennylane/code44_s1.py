# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml

def tensor_circuits():
    return qml.tape.QuantumScript([qml.CRY(0.2, wires=[0, 1]), qml.X(2)])
