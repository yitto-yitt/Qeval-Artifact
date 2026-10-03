# EVAL_META: task_id=23, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def dj_constant_oracle():
    ops = [qml.PauliX(wires=2)]
    return QuantumScript(ops)
