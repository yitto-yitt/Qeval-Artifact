# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    dev = qml.device("default.qubit", wires=range(num_qubits))

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=num_qubits - 1)
        return qml.state()

    return circuit
