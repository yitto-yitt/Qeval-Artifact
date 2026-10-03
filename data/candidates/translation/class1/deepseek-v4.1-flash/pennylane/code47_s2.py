# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)

    bits = circuit()
    total = len(bits)
    counts = {"0": 0, "1": 0}
    for bit in bits:
        counts[str(int(bit))] += 1

    return {
        "Heads": counts["0"] / total,
        "Tails": counts["1"] / total,
    }
