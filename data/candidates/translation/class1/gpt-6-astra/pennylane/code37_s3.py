# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def bv_algorithm(s):
    n = len(s)
    ancilla = n
    device = qml.device("default.qubit", wires=n + 1)

    @qml.set_shots(shots=1)
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

    result = circuit()
    samples = np.asarray(result).reshape(1, n)
    bitstrings = [
        "".join(str(int(bit)) for bit in sample[::-1])
        for sample in samples
    ]
    return [bitstrings, result]
