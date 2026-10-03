# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))

    outcomes = circuit()
    heads = int(((outcomes + 1) // 2).sum())
    tails = int(samples - heads)
    total = heads + tails
    return {"Heads": heads / total, "Tails": tails / total}
