# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml

def create_operator():
    ops = [qml.PauliX(wires=0), qml.PauliX(wires=1)]
    return qml.tape.QuantumScript(ops=ops, measurements=[])
