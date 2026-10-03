# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3)
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=range(3))
        return qml.probs(wires=range(3))
    probs = circuit()
    bitstrings = [format(i, "03b") for i in range(8)]
    return {bs: float(p) for bs, p in zip(bitstrings, probs)}
