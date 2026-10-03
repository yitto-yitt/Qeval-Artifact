# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml


def bv_algorithm(s):
    n = len(s)

    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        for wire in range(n + 1):
            qml.Hadamard(wires=wire)

        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])

        for wire in range(n):
            qml.Hadamard(wires=wire)

        return qml.sample(wires=list(range(n - 1, -1, -1)))

    samples = circuit()
    rows = samples[None, :] if samples.ndim == 1 else samples
    bitstrings = [''.join(str(int(b)) for b in row) for row in rows]

    return [bitstrings, samples]
