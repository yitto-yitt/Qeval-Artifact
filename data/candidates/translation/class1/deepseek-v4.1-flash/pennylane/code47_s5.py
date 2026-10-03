# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)

    outcomes = circuit()
    total = len(outcomes)
    ones = int(np.sum(outcomes))
    zeros = total - ones
    return {'Heads': zeros / total, 'Tails': ones / total}
