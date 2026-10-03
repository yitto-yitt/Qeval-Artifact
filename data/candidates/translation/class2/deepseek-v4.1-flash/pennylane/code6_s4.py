# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml

def create_state_prep(num_qubits):
    def state_prep():
        qml.PauliX(wires=0)
    return state_prep
