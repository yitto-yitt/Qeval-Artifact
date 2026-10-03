# EVAL_META: task_id=89, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def create_controlled_hgate():
    ops = [qml.ctrl(qml.Hadamard, control=[0, 1])(wires=2)]
    return QuantumScript(ops, [])
