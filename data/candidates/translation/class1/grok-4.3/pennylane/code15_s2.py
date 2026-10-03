# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def noisy_bell():
    dev = qml.device("default.mixed", wires=2, shots=1000)
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(0.05, wires=0)
        qml.DepolarizingChannel(0.05, wires=1)
        return qml.sample(wires=[0, 1])
    samples = bell_circuit()
    bitstrings = [''.join(map(str, s)) for s in samples]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
