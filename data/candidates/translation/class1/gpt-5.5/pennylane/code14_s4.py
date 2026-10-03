# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = Counter("".join(str(int(bit)) for bit in shot) for shot in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
