# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8, shots=1024)
    a = format(a, "08b")

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))

    samples = circuit()
    counts = {}
    for s in samples:
        key = "".join(str(int(b)) for b in reversed(s))
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
