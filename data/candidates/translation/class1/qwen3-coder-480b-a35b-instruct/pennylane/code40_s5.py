# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePreparation(desired_vector, wires=[0, 1, 2])
        return qml.sample(wires=[0, 1, 2])
    
    samples = circuit()
    
    # Count occurrences of each bitstring
    counts = {}
    num_samples = len(samples) if len(samples.shape) > 0 else 1
    
    if num_samples == 1:
        # Handle single sample case
        bitstring = ''.join(str(int(b)) for b in samples)
        counts[bitstring] = 1
    else:
        for i in range(num_samples):
            bitstring = ''.join(str(int(b)) for b in samples[i])
            counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
