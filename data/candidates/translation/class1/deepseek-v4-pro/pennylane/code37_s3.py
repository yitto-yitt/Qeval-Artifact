# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml


def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        for i in range(n + 1):
            qml.Hadamard(wires=i)

        for idx, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[idx, n])

        for i in range(n):
            qml.Hadamard(wires=i)

        return qml.counts(wires=range(n))

    counts = circuit()
    bitstrings = list(counts.keys())
    return [bitstrings, counts]
