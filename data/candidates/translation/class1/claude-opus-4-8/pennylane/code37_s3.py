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

    sample = circuit()
    bits = [int(b) for b in sample]
    bitstring = "".join(str(b) for b in reversed(bits))
    bitstrings = [bitstring]
    result = {"bitstrings": bitstrings, "sample": sample}
    return [bitstrings, result]
