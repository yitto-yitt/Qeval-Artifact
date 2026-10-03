# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as pnp

def sampler_qiskit():
    pnp.random.seed(42)
    dev = qml.device("default.qubit", wires=2, shots=1024)
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
