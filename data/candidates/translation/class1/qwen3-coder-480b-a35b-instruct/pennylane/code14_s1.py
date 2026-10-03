# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def bell_each_shot():
    dev = qml.device('default.qubit', wires=2, shots=10)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])
    
    samples = bell_circuit()
    if len(samples.shape) == 1:
        samples = samples.reshape(1, -1)
    bitstrings = ["".join(map(str, sample)) for sample in samples]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
