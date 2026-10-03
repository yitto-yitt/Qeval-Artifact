# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, seed=42)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = bell_circuit()
    # Convert samples to bitstrings
    bitstrings = ["".join(map(str, sample)) for sample in samples]
    counts = Counter(bitstrings)
    
    total = len(samples)
    return {key: value / total for key, value in counts.items()}
