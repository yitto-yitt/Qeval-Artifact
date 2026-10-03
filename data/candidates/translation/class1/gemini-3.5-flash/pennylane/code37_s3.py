# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        for i in range(n + 1):
            qml.Hadamard(wires=i)

        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])

        for i in range(n):
            qml.Hadamard(wires=i)

        return qml.sample(wires=list(range(n))[::-1])

    result = circuit()
    sample_np = np.array(result)
    if sample_np.ndim == 1:
        bitstring = "".join(str(int(x)) for x in sample_np)
    else:
        bitstring = "".join(str(int(x)) for x in sample_np[0])
    bitstrings = [bitstring]

    return [bitstrings, result]
