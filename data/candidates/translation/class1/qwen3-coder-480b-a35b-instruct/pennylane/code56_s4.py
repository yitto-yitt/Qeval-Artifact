# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def not_gate(a):
    dev = qml.device("default.qubit", wires=8, shots=None)
    
    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, "08b")
        for i in range(8):
            if a_bin[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))
    
    samples = circuit()
    # Convert samples to bitstrings
    if len(samples.shape) == 1:
        samples = samples.reshape(1, -1)
    
    bitstrings = []
    for sample in samples:
        bitstring = ''.join(str(int(b)) for b in sample)
        bitstrings.append(bitstring)
    
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
