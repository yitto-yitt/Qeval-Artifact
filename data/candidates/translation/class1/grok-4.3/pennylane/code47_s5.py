# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1)
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)
    outcomes = circuit(shots=samples)
    n_heads = 0
    n_tails = 0
    for outcome in outcomes:
        if outcome == 0:
            n_heads += 1
        else:
            n_tails += 1
    total = samples
    return {"Heads": n_heads / total, "Tails": n_tails / total}
