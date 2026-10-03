# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    def circuit():
        qml.PauliX(wires=num_qubits - 1)

    return circuit
