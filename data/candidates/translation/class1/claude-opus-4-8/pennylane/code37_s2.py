# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml


def bv_algorithm(s):
    n = len(s)
    ancilla = n
    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=ancilla)
        for w in range(n + 1):
            qml.Hadamard(wires=w)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, ancilla])
        for w in range(n):
            qml.Hadamard(wires=w)
        return qml.sample(wires=range(n))

    samples = circuit()
    samples = samples.reshape(-1, n) if n > 1 else samples.reshape(-1, 1)

    bitstrings = []
    for shot in samples:
        bits = "".join(str(int(b)) for b in reversed(list(shot)))
        bitstrings.append(bits)

    result = {"samples": samples, "bitstrings": bitstrings}
    return [bitstrings, result]
