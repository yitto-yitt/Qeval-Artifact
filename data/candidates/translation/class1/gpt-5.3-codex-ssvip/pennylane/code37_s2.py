# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml


def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n + 1, shots=1)

    @qml.qnode(dev)
    def circuit():
        ancilla = n
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
    if n == 1:
        bits = [int(samples)]
    else:
        bits = [int(b) for b in samples[0]]
    bitstring = "".join(str(b) for b in bits[::-1])
    bitstrings = [bitstring]
    result = {"samples": samples, "bitstrings": bitstrings}
    return [bitstrings, result]
