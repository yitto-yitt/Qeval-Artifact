# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np


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
        if n == 0:
            return qml.sample(wires=ancilla)
        return qml.sample(wires=list(range(n)))

    result = circuit()

    if n == 0:
        bitstrings = [""]
    else:
        samples = np.asarray(result, dtype=int).reshape(-1, n)
        bitstrings = ["".join(str(int(bit)) for bit in row[::-1]) for row in samples]

    return [bitstrings, result]
