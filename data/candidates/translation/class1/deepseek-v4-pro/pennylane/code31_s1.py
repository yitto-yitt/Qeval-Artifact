# EVAL_META: task_id=31, framework=pennylane, class=1
from typing import Dict

import pennylane as qml


def sampler_qiskit() -> Dict[str, float]:
    dev = qml.device("default.qubit", wires=2, shots=1024, seed=42)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = bell_circuit()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
