# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def create_operator():
    ops = [qml.PauliX(0), qml.PauliX(1)]
    return QuantumScript(ops, [])
