# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def not_gate(a):
    bits = format(a, "08b")
    device = qml.device("default.qubit", wires=8)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        for i in range(8):
            if bits[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=list(reversed(range(8))))

    samples = np.asarray(circuit(), dtype=int)
    counts = {}
    for sample in samples:
        key = "".join(str(bit) for bit in sample)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: count / total for key, count in counts.items()}
