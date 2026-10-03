# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[0, 1, 2])
        return qml.sample(wires=[0, 1, 2])
    
    samples = circuit()
    
    # Count occurrences of each bitstring
    counts = {}
    for sample in samples:
        bitstring = ''.join(str(int(b)) for b in sample)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = len(samples)
    return {key: value / total for key, value in counts.items()}
