# EVAL_META: task_id=49, framework=pennylane, class=3
import pennylane as qml

def simple_elitzur_vaidman():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.Hadamard(wires=0),
    ]
    return qml.tape.QuantumScript(ops=ops, measurements=[])
