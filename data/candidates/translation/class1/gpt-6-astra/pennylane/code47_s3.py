# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    device = qml.device("default.qubit", wires=1)

    @qml.set_shots(shots=samples)
    @qml.qnode(device)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.counts(wires=[0])

    counts = circuit()
    total = sum(counts.values())
    return {
        'Heads': counts.get('0', 0) / total,
        'Tails': counts.get('1', 0) / total,
    }
