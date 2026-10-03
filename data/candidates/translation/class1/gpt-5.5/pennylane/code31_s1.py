# EVAL_META: task_id=31, framework=pennylane, class=1
from typing import Dict
from collections import Counter
import pennylane as qml


def sampler_qiskit() -> Dict[str, float]:
    shots = 4096
    dev = qml.device("default.qubit", wires=2, shots=shots, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = Counter("".join(str(int(bit)) for bit in sample) for sample in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
