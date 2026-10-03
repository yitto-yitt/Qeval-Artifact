# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def tensor_circuits():
    return QuantumScript(
        ops=[
            qml.CRY(0.2, wires=[0, 1]),
            qml.PauliX(wires=2),
        ],
        measurements=[],
    )
