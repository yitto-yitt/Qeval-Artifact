# EVAL_META: task_id=31, framework=pennylane, class=1
from typing import Dict
import pennylane as qml

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, shots=1024, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
