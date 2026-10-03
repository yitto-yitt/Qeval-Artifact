# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def controlled_custom_unitary_circuit():
    custom_op = qml.ctrl(qml.U3(0.3, 0.2, 0.1, wires=1), control=0)
    return QuantumScript([custom_op])
