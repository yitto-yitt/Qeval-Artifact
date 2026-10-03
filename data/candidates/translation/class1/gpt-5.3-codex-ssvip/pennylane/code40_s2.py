# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=1024, seed=42)

    @qml.qnode(dev)
    def circuit(vec):
        qml.StatePrep(np.array(vec, dtype=complex), wires=[0, 1, 2], normalize=True)
        return qml.sample(wires=[0, 1, 2])

    samples = circuit(desired_vector)
    counts = {}
    for s in samples:
        bitstring = "".join(str(int(b)) for b in s[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
