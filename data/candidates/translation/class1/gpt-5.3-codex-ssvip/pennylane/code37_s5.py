# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml


def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n + 1, shots=1)
    ancilla = n

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
        return qml.sample(wires=list(range(n)))

    sample = circuit()
    if n == 1:
        bits = [int(sample)]
    else:
        bits = [int(b) for b in sample.tolist()]
    bitstring = "".join(str(b) for b in reversed(bits))
    bitstrings = [bitstring]
    result = {"samples": [bits], "bitstrings": bitstrings}
    return [bitstrings, result]
