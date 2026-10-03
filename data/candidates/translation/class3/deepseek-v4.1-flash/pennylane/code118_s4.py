# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def create_c3sx_circuit():
    op = qml.ctrl(qml.SX(wires=3), control=[0, 1, 2])
    return QuantumScript([op], [])
