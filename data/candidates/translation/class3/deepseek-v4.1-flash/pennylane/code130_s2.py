# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    dev = qml.device("default.qubit", wires=n)

    def original_circuit():
        for i in range(2):
            qml.Hadamard(wires=i + 1)
        for i in range(2):
            qml.CNOT(wires=[i + 1, i + 3])

    @qml.qnode(dev)
    def circuit():
        qml.adjoint(original_circuit)()
        return qml.state()

    return circuit
