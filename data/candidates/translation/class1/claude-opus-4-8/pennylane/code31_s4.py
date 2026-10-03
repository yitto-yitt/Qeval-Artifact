# EVAL_META: task_id=31, framework=pennylane, class=1
from typing import Dict
import pennylane as qml

def sampler_qiskit():
    shots = 4096
    dev = qml.device("default.qubit", wires=2, shots=shots, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = {}
    for s in samples:
        key = "".join(str(int(b)) for b in s)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
