# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml

def create_state_prep():
    def circuit():
        qml.PauliX(wires=0)
    return circuit
