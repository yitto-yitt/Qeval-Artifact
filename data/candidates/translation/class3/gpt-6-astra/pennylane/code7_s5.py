# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml


def create_parametrized_gate():
    device = qml.device("default.qubit", wires=1)

    @qml.qnode(device)
    def quantum_circuit(theta):
        qml.RX(theta, wires=0)
        return qml.state()

    return quantum_circuit
