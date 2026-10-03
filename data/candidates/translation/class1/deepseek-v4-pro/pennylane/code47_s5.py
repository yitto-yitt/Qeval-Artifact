# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device('default.qubit', wires=1, shots=samples)

    @qml.qnode(dev)
    def coin_circuit():
        qml.Hadamard(wires=0)
        return qml.counts()

    counts = coin_circuit()
    total = sum(counts.values())

    return {
        'Heads': sum(v for k, v in counts.items() if str(k) == '0') / total,
        'Tails': sum(v for k, v in counts.items() if str(k) == '1') / total,
    }
