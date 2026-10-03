# EVAL_META: task_id=31, framework=pennylane, class=1
from typing import Dict
import pennylane as qml
import numpy as np

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, shots=1024, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = {"00": 0, "01": 0, "10": 0, "11": 0}
    for s in samples:
        bitstring = f"{int(s[0])}{int(s[1])}"
        counts[bitstring] += 1

    total = len(samples)
    probs = {k: v / total for k, v in counts.items() if v > 0}
    return probs
