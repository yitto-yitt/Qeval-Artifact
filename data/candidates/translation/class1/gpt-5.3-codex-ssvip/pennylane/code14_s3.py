# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = {}
    for s in samples:
        bitstring = f"{int(s[0])}{int(s[1])}"
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
