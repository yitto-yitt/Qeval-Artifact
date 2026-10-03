# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    dev = qml.device("default.qubit", wires=2, shots=1)

    @qml.qnode(dev)
    def circuit():
        sender = 0
        receiver = 1
        qml.Hadamard(wires=sender)
        qml.CNOT(wires=[sender, receiver])
        if bitstring[1] == "1":
            qml.PauliZ(wires=sender)
        if bitstring[0] == "1":
            qml.PauliX(wires=sender)
        qml.CNOT(wires=[sender, receiver])
        qml.Hadamard(wires=sender)
        return qml.sample(wires=[sender, receiver])

    return circuit
