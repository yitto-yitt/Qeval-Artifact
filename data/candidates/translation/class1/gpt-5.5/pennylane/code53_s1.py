# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8, shots=1024)

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        for i in range(8):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        return qml.sample(wires=list(range(7, -1, -1)))

    samples = circuit()
    counts = Counter("".join(str(int(bit)) for bit in sample) for sample in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
