# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    return qml.tape.QuantumScript([
        qml.H(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.H(wires=0),
    ])
