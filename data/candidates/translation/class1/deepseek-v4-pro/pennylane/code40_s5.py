# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[2, 1, 0])
        return qml.probs(wires=[2, 1, 0])

    probs = circuit()
    return {f"{i:03b}": float(prob) for i, prob in enumerate(probs)}
