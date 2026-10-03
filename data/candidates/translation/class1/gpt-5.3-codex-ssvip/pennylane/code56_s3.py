# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def not_gate(a):
    bits = format(a, "08b")
    dev = qml.device("default.qubit", wires=8, shots=1024)

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if bits[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))

    samples = circuit()
    if samples.ndim == 1:
        samples = np.array([samples])

    counts = {}
    for s in samples:
        key = "".join(str(int(b)) for b in s[::-1])
        counts[key] = counts.get(key, 0) + 1

    total = len(samples)
    return {k: v / total for k, v in counts.items()}
