# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8, shots=1024)

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        for i in range(8):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))

    samples = circuit()
    counts = {}
    for sample in samples:
        key = ''.join(str(int(bit)) for bit in sample[::-1])
        counts[key] = counts.get(key, 0) + 1

    total = len(samples)
    return {k: v / total for k, v in counts.items()}
