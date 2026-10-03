# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    device = qml.device("default.qubit", wires=["sender", "receiver"])

    @qml.set_shots(shots=1)
    @qml.qnode(device)
    def circuit():
        qml.Hadamard(wires="sender")
        qml.CNOT(wires=["sender", "receiver"])
        qml.Barrier(wires=["sender", "receiver"])

        if bitstring[1] == "1":
            qml.PauliZ(wires="sender")
        if bitstring[0] == "1":
            qml.PauliX(wires="sender")

        qml.Barrier(wires=["sender", "receiver"])
        qml.CNOT(wires=["sender", "receiver"])
        qml.Hadamard(wires="sender")
        return qml.sample(wires=["receiver", "sender"])

    circuit()
    return circuit
