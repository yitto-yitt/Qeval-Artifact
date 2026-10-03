# EVAL_META: task_id=37, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def bv_algorithm(s):
    n = len(s)
    ancilla = n
    device = qml.device("default.qubit", wires=n + 1)

    @qml.qnode(device)
    def circuit():
        qml.PauliX(wires=ancilla)
        for wire in range(n + 1):
            qml.Hadamard(wires=wire)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, ancilla])
        for wire in range(n):
            qml.Hadamard(wires=wire)
        return qml.sample(wires=list(range(n)))

    result = qml.set_shots(circuit, shots=1)()
    samples = np.asarray(result).reshape(1, n)
    bitstrings = [
        "".join(str(int(bit)) for bit in row[::-1])
        for row in samples
    ]
    return [bitstrings, result]
