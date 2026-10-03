# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit(params):
        qml.StronglyEntanglingLayers(params, wires=range(num_qubits))
        return qml.state()

    shape = qml.StronglyEntanglingLayers.shape(n_layers=reps, n_wires=num_qubits)
    params = qml.numpy.zeros(shape)
    circuit(params)
    return circuit
