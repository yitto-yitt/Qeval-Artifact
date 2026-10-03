# EVAL_META: task_id=59, framework=pennylane, class=3
import pennylane as qml

def create_cz_gate():
    return qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=1),
            qml.CNOT(wires=[0, 1]),
            qml.Hadamard(wires=1),
        ]
    )
