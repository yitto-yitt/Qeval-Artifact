# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml


def bv_algorithm(s):
    n = len(s)
    ancilla = n
    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=ancilla)
        for wire in range(n + 1):
            qml.Hadamard(wires=wire)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, ancilla])
        for wire in range(n):
            qml.Hadamard(wires=wire)
        return qml.sample(wires=range(n))

    result = circuit()
    bitstrings = ["".join(str(int(bit)) for bit in sample[::-1]) for sample in result]
    return [bitstrings, result]
