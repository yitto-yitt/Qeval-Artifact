# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))

    results = circuit()
    total = len(results)
    heads = int(np.sum(results == 1))
    tails = int(np.sum(results == -1))
    return {"Heads": heads / total, "Tails": tails / total}
