# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml


def create_parametrized_gate():
    theta = qml.numpy.array(0.0, requires_grad=True)
    dev = qml.device("default.qubit", wires=1)

    @qml.qnode(dev)
    def quantum_circuit(theta):
        qml.RX(theta, wires=0)
        return qml.state()

    return quantum_circuit
