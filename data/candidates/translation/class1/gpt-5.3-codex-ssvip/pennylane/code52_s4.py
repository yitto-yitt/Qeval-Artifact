# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    dev = qml.device("default.qubit", wires=2, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        if bitstring[1] == "1":
            qml.PauliZ(wires=0)
        if bitstring[0] == "1":
            qml.PauliX(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        return qml.sample(wires=[0, 1])

    return circuit()
