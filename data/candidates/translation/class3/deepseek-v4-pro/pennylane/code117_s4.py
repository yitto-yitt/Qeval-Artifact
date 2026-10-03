# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml

def decompose_unitary(unitary):
    dev = qml.device('default.qubit', wires=2)

    @qml.transforms.two_qubit_decomposition
    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(unitary, wires=[0, 1])
        return qml.state()

    return circuit
