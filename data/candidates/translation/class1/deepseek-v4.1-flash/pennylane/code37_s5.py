# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n+1, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        for w in range(n+1):
            qml.Hadamard(wires=w)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
        for w in range(n):
            qml.Hadamard(wires=w)
        return qml.sample(wires=list(range(n)))

    result = circuit()
    res = np.array(result)
    if n == 1:
        res = res.reshape(1, 1)
    elif res.ndim == 1:
        res = res.reshape(1, -1)

    bitstrings = []
    for row in res:
        bits = row[::-1]
        bitstrings.append("".join(str(int(b)) for b in bits))
    return [bitstrings, result]
