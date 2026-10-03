# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=3, shots=4000, seed=42)

@qml.qnode(dev)
def circuit(desired_vector):
    qml.StatePrep(desired_vector, wires=[0, 1, 2])
    return qml.counts(wires=[0, 1, 2])

def init_random_3qubit(desired_vector):
    vec = np.array(desired_vector, dtype=complex).flatten()
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
        
    counts = circuit(vec)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
