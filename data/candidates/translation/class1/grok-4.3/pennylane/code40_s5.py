# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=1024, seed=42)
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[2, 1, 0])
        return qml.counts(wires=[2, 1, 0])
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
