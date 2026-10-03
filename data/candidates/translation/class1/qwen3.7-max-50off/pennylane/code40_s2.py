# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml

dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)
def circuit(desired_vector):
    qml.StatePrep(desired_vector, wires=[2, 1, 0])
    return qml.probs(wires=[2, 1, 0])

def init_random_3qubit(desired_vector):
    probs = circuit(desired_vector)
    return {f"{i:03b}": float(p) for i, p in enumerate(probs) if p > 1e-9}
