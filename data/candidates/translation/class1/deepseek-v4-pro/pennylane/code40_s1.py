# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[2, 1, 0])
        return qml.probs(wires=[2, 1, 0])

    probs = circuit()
    return {f"{idx:03b}": float(probs[idx]) for idx in range(8)}
