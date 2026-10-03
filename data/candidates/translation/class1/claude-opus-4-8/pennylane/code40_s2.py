# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=4096, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(np.array(desired_vector, dtype=complex), wires=range(3))
        return qml.sample(wires=range(3))

    samples = circuit()
    counts = {}
    for s in samples:
        bitstring = "".join(str(int(b)) for b in s)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
