# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)

    @qml.set_shots(shots=4096)
    @qml.qnode(dev)
    def circuit():
        for value in (a, b):
            for wire in range(8):
                if (value >> wire) & 1:
                    qml.PauliX(wires=wire)
        return qml.sample(wires=list(reversed(range(8))))

    samples = circuit()
    counts = Counter("".join(str(int(bit)) for bit in row) for row in samples)
    total = sum(counts.values())
    return {key: count / total for key, count in counts.items()}
