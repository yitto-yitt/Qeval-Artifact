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

    result = circuit()

    sample = result if hasattr(result, "shape") and result.ndim > 1 else [result]
    bitstrings = []
    for shot in sample:
        bits = "".join(str(int(b)) for b in shot)
        bitstrings.append(bits)

    return [bitstrings, result]
