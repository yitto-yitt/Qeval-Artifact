# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def tensor_circuits():
    ops = [qml.CRY(0.2, wires=[0, 1]), qml.X(2)]
    return QuantumScript(ops)
